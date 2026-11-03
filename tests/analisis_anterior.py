"""Prueba del análisis sobre resultados del formato anterior.

Escribe en una carpeta temporal resultados del formato anterior (eventos en
salida_<n>.txt, graph.adjlist y config.py por configuración, sin parametros.json
ni enlaces.csv), tomados de tests/datos/formato_anterior.json, corre
analisis/analizar.py y compara contra tests/referencia/analisis_anterior.json.

Esa referencia se comprobó contra lo que producían los scripts anteriores
(extractData.py y 1crea a 5crea): coinciden todos los archivos, salvo los
histogramas de los ciclos intermedios, que ya no llevan la tercera columna
dividida entre 2500.

Uso (desde la raíz del repositorio):
    python tests/analisis_anterior.py [--actualizar]
"""

import argparse
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from comun import compara, recoge  # noqa: E402

RAIZ = Path(__file__).resolve().parent.parent
DATOS = Path(__file__).resolve().parent / "datos" / "formato_anterior.json"
REFERENCIA = Path(__file__).resolve().parent / "referencia" / "analisis_anterior.json"


def corre():
    """Escribe los resultados de entrada, corre el análisis y regresa lo que produjo."""
    entrada = json.loads(DATOS.read_text(encoding="utf-8"))
    with tempfile.TemporaryDirectory() as tmp:
        for rel, texto in entrada.items():
            p = Path(tmp) / rel
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(texto, encoding="utf-8")
        r = subprocess.run([sys.executable, str(RAIZ / "analisis" / "analizar.py"), tmp,
                            "--pares", "200", "--workers", "2",
                            "--formato-anterior", "--figuras", tmp],
                           env=dict(os.environ, MPLBACKEND="Agg"), capture_output=True, text=True)
        if r.returncode != 0:
            raise RuntimeError(f"analizar.py terminó con error:\n{r.stderr[-3000:]}")
        return recoge(tmp, omitir=set(entrada))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--actualizar", action="store_true", help="regenera la referencia")
    args = ap.parse_args()
    obtenido = corre()
    if args.actualizar:
        REFERENCIA.write_text(json.dumps(obtenido, ensure_ascii=False, indent=0), encoding="utf-8")
        print(f"referencia actualizada: {len(obtenido)} archivos")
        return
    esperado = json.loads(REFERENCIA.read_text(encoding="utf-8"))
    sys.exit(0 if compara(esperado, obtenido) else 1)


if __name__ == "__main__":
    main()
