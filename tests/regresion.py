"""Prueba de regresión del simulador.

Corre un conjunto fijo de configuraciones pequeñas con semilla fija y compara lo
que registra el simulador (enlaces.csv: la red de cada ciclo; mensajes.csv: los
mensajes por ciclo; y resumen.json sin el tiempo) contra las referencias
guardadas en tests/referencia/. Sirve para comprobar que una refactorización no
cambia el comportamiento del simulador.

Cada caso se corre con simulador/ejecutar.py y un parametros.json que lleva la semilla.

Uso (desde la raíz del repositorio):
    python tests/regresion.py               # compara contra las referencias
    python tests/regresion.py --actualizar  # regenera las referencias (solo si
                                            # el cambio de comportamiento es intencional)
    python tests/regresion.py malla_rw_r1   # solo algunos casos
"""

import argparse
import difflib
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
REFERENCIA = Path(__file__).resolve().parent / "referencia"
SEMILLA = 12345

BASE = dict(NODOS_ANILLO=36, ROWS=6, COLUMNS=6, RED="malla", ROUTING="RANDOM-WALK",
            P=1, Q=1, REGLA=1, ALPHA=0, VECTOR_POPULARIDAD=0, VECTOR_DISTANCIA=0,
            LONG_ENLACE=1, CICLOS=3, ENLACES_DINAMICOS=2, EXPLORADORES=4, DIV_CONEXIONES=1)

R4 = dict(REGLA=4, ALPHA=0.3, VECTOR_POPULARIDAD=[1, 1, 0, 1, 0, 1, 1, 1],
          VECTOR_DISTANCIA=[0, 1, 0, 1, 1, 0, 1, 1])

# nombre -> cambios respecto a BASE
CASOS = {
    "malla_rw_r1": {},
    "malla_rw_r1_umbral0": dict(UMBRAL_R1=0.0),   # R1 sin umbral de visitas
    "malla_rw_r3_enlace0": dict(REGLA=3, UMBRAL_ENLACE=0),   # sin reconexión: los enlaces solo se llenan
    "malla_cr_r2": dict(ROUTING="COMPASS-ROUTING", REGLA=2),
    "malla_sp_r3": dict(ROUTING="SHORTEST-PATH", REGLA=3),
    "malla_rwd_r1": dict(ROUTING="RW-DEGREE"),
    "malla_rwi_r2": dict(ROUTING="RW-INVERSE", REGLA=2),
    "malla_n2v_r3": dict(ROUTING="RW-NODE2VEC", P=0.5, Q=2, REGLA=3),
    "malla_rw_r4": dict(R4),
    "malla_rw_r3_d4": dict(REGLA=3, LONG_ENLACE=4),
    "malla5x7_cr_r3_d2": dict(ROWS=5, COLUMNS=7, ROUTING="COMPASS-ROUTING", REGLA=3, LONG_ENLACE=2),
    "anillo_rw_r3": dict(RED="anillo", REGLA=3),
    "anillo_cr_r1": dict(RED="anillo", ROUTING="COMPASS-ROUTING"),
    # anillo pequeño con muchos enlaces: el diámetro llega a 2 antes del último ciclo
    "anillo16_diametro2": dict(RED="anillo", NODOS_ANILLO=16, REGLA=3, CICLOS=8,
                               ENLACES_DINAMICOS=4, EXPLORADORES=6),
    "anillo16_sin_parar": dict(RED="anillo", NODOS_ANILLO=16, REGLA=3, CICLOS=8,
                               ENLACES_DINAMICOS=4, EXPLORADORES=6, PARAR_EN_DIAMETRO_2=False),
}

GEOMETRIA = {"malla": ("ROWS", "COLUMNS"), "anillo": ("NODOS_ANILLO",)}



def conf_caso(nombre):
    conf = dict(BASE)
    conf.update(CASOS[nombre])
    return conf


def registro(carpeta):
    """Texto con lo que registró el simulador en `carpeta`, para comparar."""
    carpeta = Path(carpeta)
    resumen = json.loads((carpeta / "resumen.json").read_text(encoding="utf-8"))
    resumen.pop("tiempo_s", None)
    resumen.pop("mensajes_totales", None)  # ya está, por ciclo, en mensajes.csv
    resumen.pop("semilla", None)
    return ("## enlaces.csv\n" + (carpeta / "enlaces.csv").read_text(encoding="utf-8")
            + "## mensajes.csv\n" + (carpeta / "mensajes.csv").read_text(encoding="utf-8")
            + "## resumen.json\n" + json.dumps(resumen, sort_keys=True) + "\n")


def correr_json(nombre, codigo=RAIZ):
    """Corre un caso con simulador/ejecutar.py y parametros.json."""
    conf = conf_caso(nombre)
    parametros = dict(
        red=conf["RED"], geometria={k: conf[k] for k in GEOMETRIA[conf["RED"]]},
        routing=conf["ROUTING"], regla=conf["REGLA"], long_enlace=conf["LONG_ENLACE"],
        ciclos=conf["CICLOS"], enlaces_dinamicos=conf["ENLACES_DINAMICOS"],
        exploradores=conf["EXPLORADORES"], div_conexiones=conf["DIV_CONEXIONES"],
        p=conf["P"], q=conf["Q"], alpha=conf["ALPHA"],
        vector_popularidad=conf["VECTOR_POPULARIDAD"], vector_distancia=conf["VECTOR_DISTANCIA"],
        umbral_r1=conf.get("UMBRAL_R1", 0.5), umbral_enlace=conf.get("UMBRAL_ENLACE", 1.0),
        semilla=SEMILLA, parar_en_diametro_2=conf.get("PARAR_EN_DIAMETRO_2", True))
    with tempfile.TemporaryDirectory() as tmp:
        archivo = os.path.join(tmp, "parametros.json")
        with open(archivo, "w") as f:
            json.dump(parametros, f)
        r = subprocess.run([sys.executable, str(Path(codigo) / "simulador" / "ejecutar.py"), archivo],
                           cwd=tmp, capture_output=True, text=True)
        if r.returncode != 0:
            raise RuntimeError(f"{nombre}: ejecutar.py terminó con error\n{r.stderr[-2000:]}")
        return registro(tmp)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--actualizar", action="store_true", help="regenera las referencias")
    ap.add_argument("casos", nargs="*", help="casos a correr (por defecto, todos)")
    args = ap.parse_args()
    nombres = args.casos or list(CASOS)
    fallas = 0
    REFERENCIA.mkdir(parents=True, exist_ok=True)
    for nombre in nombres:
        salida = correr_json(nombre)
        ref = REFERENCIA / f"{nombre}.txt"
        n = salida.count("\n")
        if args.actualizar:
            ref.write_text(salida)
            print(f"actualizado  {nombre}  ({n} líneas)")
            continue
        if not ref.exists():
            print(f"SIN REFERENCIA  {nombre}")
            fallas += 1
            continue
        esperado = ref.read_text()
        if salida == esperado:
            print(f"ok      {nombre}  ({n} líneas)")
        else:
            fallas += 1
            print(f"DIFIERE {nombre}")
            diff = difflib.unified_diff(esperado.splitlines(), salida.splitlines(),
                                        "referencia", "obtenido", lineterm="", n=1)
            for linea in list(diff)[:20]:
                print("    " + linea)
    if not args.actualizar:
        print(f"\n{len(nombres) - fallas} de {len(nombres)} casos coinciden con la referencia")
    sys.exit(1 if fallas else 0)


if __name__ == "__main__":
    main()
