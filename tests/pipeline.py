"""Prueba de extremo a extremo: experimentos, simulador y análisis.

Copia el código a una carpeta temporal, configura una rejilla pequeña con semilla
fija y corre
    experimentos/formacion.py   (simulaciones: red de cada ciclo y mensajes)
    analisis/analizar.py        (medidas y promedios; figuras y GEXF de una corrida)
y compara todos los archivos de resultados contra tests/referencia/pipeline.json.
De las imágenes PNG solo comprueba que existan; se ignoran el tiempo de
ejecución y las líneas con fecha que escribe networkx.

Uso (desde la raíz del repositorio):
    python tests/pipeline.py               # compara contra la referencia
    python tests/pipeline.py --actualizar  # regenera la referencia
    python tests/pipeline.py --conservar   # no borra la carpeta temporal (para revisar)

Tarda alrededor de 1 minuto.
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from comun import compara, recoge  # noqa: E402

RAIZ = Path(__file__).resolve().parent.parent
REFERENCIA = Path(__file__).resolve().parent / "referencia" / "pipeline.json"

# Se agregan al final de la copia de experimentos/configuracion.py
CONFIGURACION = """
#--- Valores de la prueba de pipeline (tests/pipeline.py) ---
BASE_DIR = {base!r}
RESULTADOS_DIR = BASE_DIR + "Formacion"
NODOS_ANILLO = 36
ROWS = 6
COLUMNS = 6
RED = ["malla", "anillo"]
ROUTING = ["RANDOM-WALK", "COMPASS-ROUTING", "RW-NODE2VEC"]
PQ_NODE2VEC = [(0.5, 2)]
REGLAS = [1, 3]
LONG_ENLACES = [1, 2]
CICLOS = 2
EJECUCIONES = 3
ENLACES_DINAMICOS = 2
EXPLORADORES = 4
DIV_CONEXIONES = 1
SEMILLA_BASE = 7
NUM_WORKERS = 2
"""


def corre_pipeline(trabajo):
    for carpeta in ("simulador", "experimentos", "analisis"):
        shutil.copytree(RAIZ / carpeta, trabajo / carpeta, ignore=shutil.ignore_patterns("__pycache__"))
    with open(trabajo / "experimentos" / "configuracion.py", "a", encoding="utf-8") as f:
        f.write(CONFIGURACION.format(base=str(trabajo / "resultados") + "/"))
    entorno = dict(os.environ, MPLBACKEND="Agg")
    for comando in (["experimentos/formacion.py"], ["analisis/analizar.py", "--pares", "200", "--figuras", "malla6x6/R1/RW/D1/1"]):
        r = subprocess.run([sys.executable] + comando, cwd=trabajo, env=entorno, capture_output=True, text=True)
        if r.returncode != 0:
            raise RuntimeError(f"{comando[0]} terminó con error:\n{r.stderr[-3000:]}")
        print(f"  corrió {comando[0]}")
    return recoge(trabajo / "resultados" / "Formacion")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--actualizar", action="store_true", help="regenera la referencia")
    ap.add_argument("--conservar", action="store_true", help="no borra la carpeta temporal")
    args = ap.parse_args()
    trabajo = Path(tempfile.mkdtemp(prefix="pipeline_"))
    try:
        obtenido = corre_pipeline(trabajo)
    finally:
        if args.conservar:
            print(f"carpeta temporal: {trabajo}")
        else:
            shutil.rmtree(trabajo, ignore_errors=True)
    if args.actualizar:
        REFERENCIA.parent.mkdir(parents=True, exist_ok=True)
        REFERENCIA.write_text(json.dumps(obtenido, ensure_ascii=False, indent=0), encoding="utf-8")
        print(f"referencia actualizada: {len(obtenido)} archivos")
        return
    esperado = json.loads(REFERENCIA.read_text(encoding="utf-8"))
    sys.exit(0 if compara(esperado, obtenido) else 1)


if __name__ == "__main__":
    main()
