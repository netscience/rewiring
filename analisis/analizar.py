"""
Analiza todos los resultados de una carpeta.

Uso (desde la raíz del repositorio):
    python analisis/analizar.py [carpeta_resultados] [opciones]

Sin carpeta, usa RESULTADOS_DIR de experimentos/configuracion.py. Pasos:

  1. Cada corrida (en paralelo): reconstruye la red de cada ciclo y calcula todas
     las medidas -> metricas_ciclo.csv, navegabilidad.csv, longitudes_enlaces.csv.
  2. Cada configuración: promedios sobre las ejecuciones -> metricas-promedio.csv,
     estado-final.csv.
  3. Tabla global estado_final.csv (una fila por configuración).

Opciones:
  --pares N            pares para la navegabilidad (por omisión 2000)
  --workers N          procesos en paralelo (por omisión, los de configuracion.py o 4)
  --formato-anterior   además, los archivos de los scripts anteriores: datos-salida,
                       hist_test y graph_test por corrida, datos-promedio*.csv por
                       configuración y las tablas Medidas_estructurales/
  --figuras RUTA ...   PNG y GEXF de la red final, solo de las corridas que estén bajo
                       las rutas dadas (absolutas o relativas a la carpeta de resultados),
                       p.e. --figuras malla8x8/R1/RW/D1/1 anillo64/R3
  --escala-nodos X     tamaño de los nodos en las imágenes (por omisión, según el tamaño de la red)
"""

import argparse
import csv
import sys
from functools import partial
import multiprocessing
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

if not __package__:
    # Corrido como archivo (python analisis/analizar.py), o como módulo principal de un proceso
    # hijo de multiprocessing ("spawn", el modo por omisión en macOS y Windows):
    # se importa como paquete para que funcionen las importaciones relativas
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    __package__ = "analisis"
    import analisis  # noqa: F401

from .figuras import figuras_corrida
from .lectura import configuraciones, ejecuciones
from .por_corrida import _fmt, analiza_corrida
from .promedios import analiza_configuracion, fila_resumen
from .tablas import crea_tablas


def _configuracion_experimentos():
    """experimentos/configuracion.py, si existe (solo para la carpeta y los workers por omisión)."""
    archivo = Path(__file__).resolve().parent.parent / "experimentos" / "configuracion.py"
    if not archivo.exists():
        return {}
    datos = {}
    exec(compile(archivo.read_text(encoding="utf-8"), str(archivo), "exec"), datos)
    return datos


def _corrida(carpeta, pares, formato_anterior):
    analiza_corrida(carpeta, pares=pares, formato_anterior=formato_anterior)
    return carpeta


def _figuras(carpeta, escala):
    figuras_corrida(carpeta, escala=escala)
    return carpeta


def _en_paralelo(pool, funcion, corridas, etiqueta):
    """Aplica `funcion` a cada corrida en el pool y muestra el avance. Si una
    corrida falla, se detiene con el error y la carpeta de esa corrida."""
    futuros = {pool.submit(funcion, d): d for d in corridas}
    for i, futuro in enumerate(as_completed(futuros), 1):
        try:
            futuro.result()
        except Exception as e:
            for f in futuros:
                f.cancel()
            raise RuntimeError(f"{etiqueta}: falló la corrida {futuros[futuro]}: {e!r}") from e
        if i % 50 == 0 or i == len(corridas):
            print(f"  {etiqueta}: {i} de {len(corridas)} corridas", flush=True)


def _bajo(carpeta, rutas):
    carpeta = carpeta.resolve()
    return any(carpeta == r or r in carpeta.parents for r in rutas)


def analizar(resultados, pares=2000, workers=4, formato_anterior=False, figuras=(), escala=None):
    """Analiza la carpeta `resultados`. `figuras` es una lista de rutas: se hacen
    PNG y GEXF de las corridas que estén bajo alguna de ellas."""
    resultados = Path(resultados)
    configs = configuraciones(resultados)
    corridas = [d for c in configs for d in ejecuciones(c)]
    print(f"{len(configs)} configuraciones, {len(corridas)} corridas en {resultados}")
    rutas = [(Path(r) if Path(r).is_absolute() else resultados / r).resolve() for r in figuras]
    con_figuras = [d for d in corridas if _bajo(d, rutas)]
    if figuras and not con_figuras:
        print(f"  aviso: ninguna corrida está bajo {list(figuras)}; no se harán figuras")

    # Siempre "spawn": igual en Linux que en macOS (donde es el modo por omisión),
    # para que las pruebas en cualquier sistema cubran el mismo camino. Con
    # ProcessPoolExecutor, si un proceso hijo falla el análisis se detiene con el
    # error en lugar de quedarse esperando.
    with ProcessPoolExecutor(max_workers=workers, mp_context=multiprocessing.get_context("spawn")) as pool:
        _en_paralelo(pool, partial(_corrida, pares=pares, formato_anterior=formato_anterior), corridas, "medidas")

        filas = []
        for c in configs:
            primera, finales = analiza_configuracion(c, formato_anterior)
            filas.append(fila_resumen(c, str(c.relative_to(resultados)), primera, finales))
        if filas:
            columnas = list(filas[0])
            with open(resultados / "estado_final.csv", "w", newline="", encoding="utf-8") as f:
                w = csv.writer(f)
                w.writerow(columnas)
                for fila in filas:
                    w.writerow([_fmt(fila.get(k)) for k in columnas])
        print("  promedios y estado_final.csv listos", flush=True)
        if formato_anterior:
            crea_tablas(resultados, configs)
            print("  tablas Medidas_estructurales listas", flush=True)

        if con_figuras:
            _en_paralelo(pool, partial(_figuras, escala=escala), con_figuras, "figuras")
    print("Análisis terminado.")


def main():
    cfg = _configuracion_experimentos()
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("resultados", nargs="?", default=cfg.get("RESULTADOS_DIR"))
    ap.add_argument("--pares", type=int, default=2000)
    ap.add_argument("--workers", type=int, default=cfg.get("NUM_WORKERS", 4))
    ap.add_argument("--formato-anterior", action="store_true")
    ap.add_argument("--figuras", nargs="+", default=[], metavar="RUTA")
    ap.add_argument("--escala-nodos", type=float, default=None)
    args = ap.parse_args()
    if not args.resultados:
        ap.error("indica la carpeta de resultados")
    analizar(args.resultados, args.pares, args.workers, args.formato_anterior, args.figuras, args.escala_nodos)


if __name__ == "__main__":
    main()
