"""Corre todas las pruebas: unidades, regresión del simulador, análisis del formato
anterior y pipeline completo.

Uso (desde la raíz del repositorio):
    python tests/correr_todas.py            # todas (unos 3 a 5 minutos)
    python tests/correr_todas.py --rapidas  # sin el pipeline (menos de un minuto)
"""

import subprocess
import sys
from pathlib import Path

PRUEBAS = Path(__file__).resolve().parent


def main():
    rapidas = "--rapidas" in sys.argv
    lista = ["unidades.py", "regresion.py"] + ([] if rapidas else ["analisis_anterior.py", "pipeline.py"])
    resultados = {}
    for prueba in lista:
        print(f"\n===== {prueba} =====", flush=True)
        r = subprocess.run([sys.executable, str(PRUEBAS / prueba)], cwd=PRUEBAS.parent)
        resultados[prueba] = r.returncode == 0
    print("\n===== Resumen =====")
    for prueba, ok in resultados.items():
        print(f"  {'ok     ' if ok else 'FALLA  '} {prueba}")
    sys.exit(0 if all(resultados.values()) else 1)


if __name__ == "__main__":
    main()
