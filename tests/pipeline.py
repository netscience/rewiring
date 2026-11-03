"""Prueba de extremo a extremo del pipeline de experimentos y de los scripts de análisis.

Copia el código a una carpeta temporal, configura una rejilla pequeña con semilla fija
y corre, en orden:

    formacion.py
    1creaPromediosFormacion.py  2creaPromediosDistGradosFormacion.py
    3creaImagenesPNG.py  4creaGEXF.py  5creaTablasFormacion.py

Después compara todos los archivos de resultados contra tests/referencia/pipeline.json:
la estructura de carpetas, la salida del simulador, los archivos de extractData
(métricas por ciclo, histogramas, grafos por ciclo), los promedios, las tablas y los
GEXF. De las imágenes PNG solo comprueba que existan. Se ignoran los tiempos
(metricas_rendimiento.csv), los logs, los archivos .py y las líneas de comentario
con fecha o versión que escribe networkx.

Congela el comportamiento ACTUAL, incluidos estos errores conocidos de los scripts de
análisis (se corregirán en el paso 3 de la refactorización, regenerando la referencia):
  - extractData.py normaliza los histogramas intermedios entre 2500 (malla de 50x50).

Uso (desde la raíz del repositorio):
    python tests/pipeline.py               # compara contra la referencia
    python tests/pipeline.py --actualizar  # regenera la referencia
    python tests/pipeline.py --conservar   # no borra la carpeta temporal (para revisar)

Tarda alrededor de 2 a 4 minutos.
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
REFERENCIA = Path(__file__).resolve().parent / "referencia" / "pipeline.json"

SCRIPTS = ["formacion.py",
           "1creaPromediosFormacion.py", "2creaPromediosDistGradosFormacion.py",
           "3creaImagenesPNG.py", "4creaGEXF.py", "5creaTablasFormacion.py"]

# Se agregan al final de la copia de configuracion.py (sustituyen los valores del usuario)
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

IGNORAR = re.compile(r"(\.py$|\.pyc$|__pycache__|log_\d+\.txt$|metricas_rendimiento\.csv$)")


def normaliza(ruta, texto):
    """Quita lo que cambia entre máquinas o días sin cambiar los resultados."""
    if ruta.endswith(".adjlist"):
        # networkx escribe comentarios con la línea de comandos y la fecha
        return "\n".join(l for l in texto.splitlines() if not l.startswith("#")) + "\n"
    if ruta.endswith(".gexf"):
        texto = re.sub(r'lastmodifieddate="[^"]*"', 'lastmodifieddate=""', texto)
        texto = re.sub(r"<creator>.*?</creator>", "<creator/>", texto)
    return texto


def recoge(resultados):
    """Diccionario ruta relativa -> contenido normalizado (o marca de existencia)."""
    salida = {}
    for raiz, dirs, archivos in os.walk(resultados):
        dirs[:] = [d for d in dirs if d != "__pycache__"]
        for nombre in archivos:
            completa = os.path.join(raiz, nombre)
            rel = os.path.relpath(completa, resultados)
            if IGNORAR.search(rel):
                continue
            if nombre.endswith(".png"):
                salida[rel] = "<png>"
            else:
                with open(completa, encoding="utf-8", errors="replace") as f:
                    salida[rel] = normaliza(rel, f.read())
    return dict(sorted(salida.items()))


def corre_pipeline(trabajo):
    for archivo in RAIZ.glob("*.py"):
        shutil.copy2(archivo, trabajo)
    with open(trabajo / "configuracion.py", "a", encoding="utf-8") as f:
        f.write(CONFIGURACION.format(base=str(trabajo / "resultados") + "/"))
    entorno = dict(os.environ, MPLBACKEND="Agg")
    for script in SCRIPTS:
        r = subprocess.run([sys.executable, script], cwd=trabajo, env=entorno,
                           capture_output=True, text=True)
        if r.returncode != 0:
            raise RuntimeError(f"{script} terminó con error:\n{r.stderr[-3000:]}")
        print(f"  corrió {script}")
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
    faltan = sorted(set(esperado) - set(obtenido))
    sobran = sorted(set(obtenido) - set(esperado))
    distintos = sorted(k for k in set(esperado) & set(obtenido) if esperado[k] != obtenido[k])
    for titulo, lista in (("Faltan", faltan), ("Sobran", sobran), ("Distintos", distintos)):
        if lista:
            print(f"{titulo} ({len(lista)}):")
            for k in lista[:15]:
                print(f"    {k}")
            if len(lista) > 15:
                print(f"    ... y {len(lista) - 15} más")
    iguales = len(set(esperado) & set(obtenido)) - len(distintos)
    print(f"\n{iguales} de {len(esperado)} archivos coinciden con la referencia")
    sys.exit(0 if not (faltan or sobran or distintos) else 1)


if __name__ == "__main__":
    main()
