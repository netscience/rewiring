"""
Corre una serie de experimentos de formación de redes definida en configuracion.py.

Uso:
    python formacion.py

Para cada combinación de red, regla, exploración y longitud de enlace crea la
carpeta RESULTADOS_DIR/<red>/R<regla>/<exploración>/D<long_enlace> y, dentro,
una subcarpeta por ejecución (1, 2, ...). En cada ejecución escribe
parametros.json, corre ejecutar.py (sin copiar el código del simulador) y
después extractData.py. Las configuraciones se reparten entre NUM_WORKERS
procesos en paralelo; cada corrida es un proceso de Python independiente.

Archivos de cada ejecución <n>:
    parametros.json, graph.adjlist, semilla.txt, metricas_rendimiento.csv,
    salida_<n>.txt (eventos), y los de extractData.py: datos-salida_<n>.txt,
    hist_test_<c>.txt, graph_test_<c>.adjlist.
"""

import os
import subprocess
import sys
import zlib
from dataclasses import replace
from multiprocessing import Pool
from pathlib import Path

import configuracion
import redes
from parametros import Parametros

RAIZ = Path(__file__).resolve().parent   # Carpeta del código del simulador
PYTHON_EXEC = sys.executable             # Mismo intérprete que corre este script

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
        for r in configuracion.REGLAS:
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
                        ruta = f"{configuracion.RESULTADOS_DIR}/{red_obj.nombre()}/R{r}/{carpeta}/D{long_enlace}"
                        par = Parametros(
                            red=red_obj.CLAVE, geometria=geometria, routing=ruteo, regla=r,
                            long_enlace=long_enlace, ciclos=configuracion.CICLOS,
                            enlaces_dinamicos=configuracion.ENLACES_DINAMICOS,
                            exploradores=configuracion.EXPLORADORES,
                            div_conexiones=configuracion.DIV_CONEXIONES, p=p, q=q)
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
        salida = f"salida_{x}.txt"
        with open(hoja / salida, "w", encoding="utf-8") as out_f:
            r = subprocess.run([PYTHON_EXEC, str(RAIZ / "ejecutar.py"), "parametros.json"],
                               cwd=hoja, stdout=out_f)
        if r.returncode != 0:
            print(f" ERROR: la simulación terminó con código {r.returncode} en {hoja}")
            continue
        subprocess.run([PYTHON_EXEC, str(RAIZ / "extractData.py"), salida, "test"], cwd=hoja)
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
    with Pool(processes=num_workers) as pool:
        pool.map(ejecutar_configuracion, tareas)
    print("\n¡Simulaciones de formación completadas con éxito!")
