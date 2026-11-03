"""
Corre una serie de experimentos de formación de redes definida en configuracion.py.

Uso (desde la raíz del repositorio):
    python experimentos/formacion.py

Para cada combinación de red, regla (con sus umbrales), exploración y longitud
de enlace crea la carpeta RESULTADOS_DIR/<red>/R<regla>[u..][e..]/<exploración>/D<long_enlace> y, dentro,
una subcarpeta por ejecución (1, 2, ...). En cada ejecución escribe
parametros.json y corre el simulador (simulador/ejecutar.py), que registra la
red de cada ciclo y los mensajes (ver simulador/salida.py). No hace ningún
análisis: después se corre analisis/analizar.py sobre RESULTADOS_DIR.

Las configuraciones se reparten entre NUM_WORKERS procesos en paralelo; cada
corrida es un proceso de Python independiente.
"""

import os
import subprocess
import sys
import zlib
from dataclasses import replace
import multiprocessing
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

AQUI = Path(__file__).resolve().parent   # Carpeta experimentos/ (configuracion.py)
RAIZ = AQUI.parent                       # Raíz del repositorio (paquete simulador/)
for _ruta in (str(AQUI), str(RAIZ)):
    if _ruta not in sys.path:
        sys.path.insert(0, _ruta)

import configuracion  # noqa: E402
from simulador import redes  # noqa: E402
from simulador.parametros import Parametros  # noqa: E402

PYTHON_EXEC = sys.executable             # Mismo intérprete que corre este script
ENTORNO = dict(os.environ, PYTHONPATH=str(RAIZ) + os.pathsep + os.environ.get("PYTHONPATH", ""))

# Abreviatura de cada exploración en los nombres de carpeta
ABREVIATURAS = {
    "COMPASS-ROUTING": "CR",
    "RANDOM-WALK": "RW",
    "RW-DEGREE": "RWD",
    "RW-INVERSE": "RWI",
    "RW-NODE2VEC": "N2V",
    "SHORTEST-PATH": "SP",
}


def semilla_corrida(ruta, ejecucion):
    """Semilla reproducible de una corrida, o None si SEMILLA_BASE es None.

    Depende de la base, de la ruta de la configuración relativa a
    RESULTADOS_DIR y del número de ejecución, de modo que cada corrida tiene
    una semilla distinta y la misma en cualquier máquina."""
    base = getattr(configuracion, "SEMILLA_BASE", None)
    if base is None:
        return None
    relativa = os.path.relpath(ruta, configuracion.RESULTADOS_DIR)
    return (int(base) * 1000003 + zlib.crc32(f"{relativa}|{ejecucion}".encode())) % (2**32)


UMBRAL_ENLACE_OMISION = 1.0
UMBRAL_R1_OMISION = 0.5


def _lista(valor):
    """Acepta un valor suelto o una lista de valores."""
    return list(valor) if isinstance(valor, (list, tuple)) else [valor]


def _texto_num(x):
    """0.25 -> "0_25", 1.0 -> "1" (para nombres de carpeta)."""
    x = float(x)
    return str(int(x)) if x.is_integer() else str(x).replace(".", "_")


def carpeta_regla(r, umbral_r1, umbral_enlace):
    """Nombre de la carpeta de la regla: R<r>, más un sufijo por cada umbral que no
    tenga su valor por omisión (u: UMBRAL_R1, solo en R1; e: UMBRAL_ENLACE)."""
    nombre = f"R{r}"
    if r == 1 and float(umbral_r1) != UMBRAL_R1_OMISION:
        nombre += "u" + _texto_num(umbral_r1)
    if float(umbral_enlace) != UMBRAL_ENLACE_OMISION:
        nombre += "e" + _texto_num(umbral_enlace)
    return nombre


def valida_configuracion():
    """Regresa la lista de errores en las listas de configuracion.py (vacía si no hay)."""
    errores = []
    for nombre, valores, validos in (("RED", configuracion.RED, list(redes.REDES)),
                                     ("ROUTING", configuracion.ROUTING, list(ABREVIATURAS)),
                                     ("REGLAS", configuracion.REGLAS, [1, 2, 3, 4])):
        if not isinstance(valores, (list, tuple)):
            errores.append(f"{nombre} debe ser una lista, p.e. {nombre} = [{validos[0]!r}]")
            continue
        for v in valores:
            if v not in validos:
                consejo = ""
                if isinstance(v, str) and "," in v:
                    partes = ", ".join(repr(x.strip()) for x in v.split(","))
                    consejo = f" (¿quisiste escribir {nombre} = [{partes}]?)"
                errores.append(f"{nombre}: valor desconocido {v!r}{consejo}. Válidos: {validos}")
    for nombre in ("UMBRAL_ENLACE", "UMBRAL_R1"):
        for v in _lista(getattr(configuracion, nombre, [])):
            if not isinstance(v, (int, float)) or isinstance(v, bool) or v < 0:
                errores.append(f"{nombre}: {v!r} no es un número mayor o igual que 0")
    return errores


def plan():
    """Lista de (ruta, Parametros) con todas las configuraciones de configuracion.py.
    Los parámetros no llevan semilla; se asigna una por ejecución."""
    tareas = []
    for red in configuracion.RED:
        try:
            red_obj = redes.obtener_red(red, configuracion)
        except ValueError:
            print(f" Tipo de red desconocido, saltando: {red}")
            continue
        geometria = {n: getattr(configuracion, n) for n in red_obj.PARAMETROS}
        umbrales_enlace = _lista(getattr(configuracion, "UMBRAL_ENLACE", UMBRAL_ENLACE_OMISION))
        umbrales_r1 = _lista(getattr(configuracion, "UMBRAL_R1", UMBRAL_R1_OMISION))
        # (regla, umbral_r1, umbral_enlace): UMBRAL_R1 solo varía en R1
        reglas = [(r, u, e) for r in configuracion.REGLAS
                  for u in (umbrales_r1 if r == 1 else [UMBRAL_R1_OMISION])
                  for e in umbrales_enlace]
        for r, umbral_r1, umbral_enlace in reglas:
            regla = carpeta_regla(r, umbral_r1, umbral_enlace)
            for ruteo in configuracion.ROUTING:
                if ruteo not in ABREVIATURAS:
                    print(f" Algoritmo de ruteo desconocido, saltando: {ruteo}")
                    continue
                # Node2Vec se corre para cada pareja (p, q); las demás exploraciones no usan p ni q
                if ruteo == "RW-NODE2VEC":
                    variantes = [(p, q, ABREVIATURAS[ruteo] + "p" + str(p).replace(".", "_") + "q" + str(q).replace(".", "_"))
                                 for p, q in configuracion.PQ_NODE2VEC]
                else:
                    variantes = [(0, 0, ABREVIATURAS[ruteo])]
                for long_enlace in configuracion.LONG_ENLACES:
                    for p, q, carpeta in variantes:
                        ruta = f"{configuracion.RESULTADOS_DIR}/{red_obj.nombre()}/{regla}/{carpeta}/D{long_enlace}"
                        par = Parametros(
                            red=red_obj.CLAVE, geometria=geometria, routing=ruteo, regla=r,
                            long_enlace=long_enlace, ciclos=configuracion.CICLOS,
                            enlaces_dinamicos=configuracion.ENLACES_DINAMICOS,
                            exploradores=configuracion.EXPLORADORES,
                            div_conexiones=configuracion.DIV_CONEXIONES, p=p, q=q,
                            umbral_r1=umbral_r1, umbral_enlace=umbral_enlace)
                        if r == 4:
                            par = replace(par, alpha=configuracion.ALPHA,
                                          vector_popularidad=configuracion.VECTOR_POPULARIDAD,
                                          vector_distancia=configuracion.VECTOR_DISTANCIA)
                        tareas.append((ruta, par))
    return tareas


def ejecutar_configuracion(tarea):
    """Corre todas las ejecuciones de una configuración, una tras otra."""
    ruta, par = tarea
    print(f"\n>>> Iniciando configuración en: {ruta}")
    for x in range(1, configuracion.EJECUCIONES + 1):
        hoja = Path(ruta) / str(x)
        hoja.mkdir(parents=True, exist_ok=True)
        print(f" - Simulación {x} en: {hoja}")

        replace(par, semilla=semilla_corrida(ruta, x)).guardar(hoja / "parametros.json")
        r = subprocess.run([PYTHON_EXEC, "-m", "simulador.ejecutar", "parametros.json"],
                           cwd=hoja, env=ENTORNO)
        if r.returncode != 0:
            print(f" ERROR: la simulación terminó con código {r.returncode} en {hoja}")
    print(f"<<< Finalizada configuración en: {ruta}")


if __name__ == "__main__":
    errores = valida_configuracion()
    if errores:
        print("Error en configuracion.py:")
        for e in errores:
            print("  - " + e)
        raise SystemExit(1)
    tareas = plan()
    num_workers = getattr(configuracion, "NUM_WORKERS", 4)
    print(f"\nEjecutando {len(tareas)} configuraciones en paralelo usando {num_workers} workers...")
    # Siempre "spawn", el modo por omisión en macOS, también en Linux. Con
    # ProcessPoolExecutor, si un proceso hijo falla se detiene con el error en
    # lugar de quedarse esperando.
    with ProcessPoolExecutor(max_workers=num_workers, mp_context=multiprocessing.get_context("spawn")) as pool:
        list(pool.map(ejecutar_configuracion, tareas))
    print("\n¡Simulaciones de formación completadas con éxito!")
