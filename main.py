"""
Compatibilidad con el formato anterior: corre una simulación a partir de un
config.py (constantes en mayúsculas) que esté en el directorio de trabajo.

Uso:
    python main.py [archivo_log] [semilla]

Los archivos de la corrida (graph.adjlist, semilla.txt,
metricas_rendimiento.csv) se escriben en la carpeta de archivo_log, o en la
carpeta actual si no se da. La semilla también puede venir de config.SEMILLA.

Para los experimentos nuevos usar ejecutar.py con un parametros.json.
"""

import sys
from pathlib import Path

import config
from ejecutar import simular
from parametros import Parametros

if __name__ == "__main__":
    semilla = int(sys.argv[2]) if len(sys.argv) > 2 else None
    carpeta = Path(sys.argv[1]).parent if len(sys.argv) > 1 else Path(".")
    simular(Parametros.desde_config(config, semilla), carpeta)
