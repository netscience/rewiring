"""Prueba de regresión del simulador.

Corre un conjunto fijo de configuraciones pequeñas con semilla fija y compara
la salida (las líneas de conexión y reconexión que imprime main.py) contra las
salidas de referencia guardadas en tests/referencia/. Sirve para comprobar que
una refactorización no cambia el comportamiento del simulador.

Uso (desde la raíz del repositorio):
    python tests/regresion.py               # compara contra las referencias
    python tests/regresion.py --actualizar  # regenera las referencias (solo si
                                            # el cambio de comportamiento es intencional)
    python tests/regresion.py --codigo DIR  # prueba el código de otra carpeta
                                            # (p.e. una versión anterior; añadir
                                            # --red-numerica si usa RED = 1 o 3)

Cada caso se corre de dos maneras y ambas deben dar la referencia:
  - con ejecutar.py y un parametros.json que lleva la semilla (la forma actual);
  - con main.py y un config.py, fijando la semilla desde fuera de main.py, de
    modo que también sirve para versiones del código que no aceptan semilla.
Con --codigo se usa solo main.py si esa carpeta no tiene ejecutar.py.
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
}

ENVOLTURA = """import random, sys, runpy
import numpy
sys.path[:0] = [{tmp!r}, {codigo!r}]
random.seed({semilla}); numpy.random.seed({semilla})
sys.argv = [{main!r}, {log!r}]
runpy.run_path({main!r}, run_name="__main__")
"""


def correr(nombre, codigo, red_numerica=False):
    """Corre un caso y regresa su salida estándar."""
    conf = dict(BASE)
    conf.update(CASOS[nombre])
    if red_numerica:  # versiones anteriores a redes.py: 1 = malla, 3 = anillo
        conf["RED"] = {"malla": 1, "anillo": 3}[conf["RED"]]
    with tempfile.TemporaryDirectory() as tmp:
        with open(os.path.join(tmp, "config.py"), "w") as f:
            for k, v in conf.items():
                f.write(f"{k} = {v!r}\n")
        log = os.path.join(tmp, "log.txt")
        open(log, "w").close()
        envoltura = os.path.join(tmp, "_correr.py")
        with open(envoltura, "w") as f:
            f.write(ENVOLTURA.format(tmp=tmp, codigo=str(codigo), semilla=SEMILLA,
                                     main=str(Path(codigo) / "main.py"), log=log))
        r = subprocess.run([sys.executable, envoltura], cwd=tmp, capture_output=True, text=True)
        if r.returncode != 0:
            raise RuntimeError(f"{nombre}: main.py terminó con error\n{r.stderr[-2000:]}")
        return r.stdout


GEOMETRIA = {"malla": ("ROWS", "COLUMNS"), "anillo": ("NODOS_ANILLO",)}


def correr_json(nombre, codigo):
    """Corre un caso con ejecutar.py y parametros.json; regresa su salida estándar."""
    conf = dict(BASE)
    conf.update(CASOS[nombre])
    parametros = dict(
        red=conf["RED"], geometria={k: conf[k] for k in GEOMETRIA[conf["RED"]]},
        routing=conf["ROUTING"], regla=conf["REGLA"], long_enlace=conf["LONG_ENLACE"],
        ciclos=conf["CICLOS"], enlaces_dinamicos=conf["ENLACES_DINAMICOS"],
        exploradores=conf["EXPLORADORES"], div_conexiones=conf["DIV_CONEXIONES"],
        p=conf["P"], q=conf["Q"], alpha=conf["ALPHA"],
        vector_popularidad=conf["VECTOR_POPULARIDAD"], vector_distancia=conf["VECTOR_DISTANCIA"],
        semilla=SEMILLA)
    with tempfile.TemporaryDirectory() as tmp:
        archivo = os.path.join(tmp, "parametros.json")
        with open(archivo, "w") as f:
            json.dump(parametros, f)
        r = subprocess.run([sys.executable, str(Path(codigo) / "ejecutar.py"), archivo],
                           cwd=tmp, capture_output=True, text=True)
        if r.returncode != 0:
            raise RuntimeError(f"{nombre}: ejecutar.py terminó con error\n{r.stderr[-2000:]}")
        return r.stdout


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--actualizar", action="store_true", help="regenera las referencias")
    ap.add_argument("--codigo", default=str(RAIZ), help="carpeta con el código a probar")
    ap.add_argument("--red-numerica", action="store_true",
                    help="escribe RED como número (1 malla, 3 anillo), para versiones anteriores a redes.py")
    ap.add_argument("casos", nargs="*", help="casos a correr (por defecto, todos)")
    args = ap.parse_args()
    nombres = args.casos or list(CASOS)
    fallas = 0
    REFERENCIA.mkdir(parents=True, exist_ok=True)
    con_json = (Path(args.codigo) / "ejecutar.py").exists()
    for nombre in nombres:
        salida = correr(nombre, args.codigo, args.red_numerica)
        if con_json:
            salida_json = correr_json(nombre, args.codigo)
            if salida_json != salida:
                fallas += 1
                print(f"DIFIERE {nombre}: ejecutar.py con parametros.json no da lo mismo que main.py con config.py")
                continue
        ref = REFERENCIA / f"{nombre}.txt"
        if args.actualizar:
            ref.write_text(salida)
            print(f"actualizado  {nombre}  ({len(salida.splitlines())} líneas)")
            continue
        if not ref.exists():
            print(f"SIN REFERENCIA  {nombre}")
            fallas += 1
            continue
        esperado = ref.read_text()
        if salida == esperado:
            print(f"ok      {nombre}  ({len(salida.splitlines())} líneas)")
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
