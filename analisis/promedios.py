"""
Promedios sobre las ejecuciones de una configuración.

  metricas-promedio.csv      todas las medidas de metricas_ciclo.csv por ciclo:
                             media e intervalo de confianza al 95 %
  estado-final.csv           estado final de cada ejecución (promedio de los
                             últimos ULTIMOS ciclos de cada medida, sin contar la
                             red base) y su navegabilidad

y, con formato_anterior:

  datos-promedio.csv         agrupamiento, ASPL y diámetro por ciclo: media y
                             desviación estándar
  datos-promedio_grados.csv  distribución de grados promedio de la red final

Si una ejecución terminó antes (el diámetro llegó a 2), sus últimos valores se
repiten hasta completar los ciclos, como hacía 1creaPromediosFormacion.py.
"""

import csv
import math

import numpy as np

from . import medidas
from .lectura import Corrida, ejecuciones
from .por_corrida import COLUMNAS, _fmt

ULTIMOS = 5   # ciclos que se promedian para el estado final
MEDIDAS = [c for c in COLUMNAS if c != "ciclo"]
NAVEGABILIDAD = ["exito", "pasos_medios", "estiramiento"]


def _lee_csv(archivo):
    with open(archivo, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _num(x):
    return float(x) if x not in ("", None) else float("nan")


def _serie(filas, medida, ciclos):
    """Valores de una medida en los ciclos 0..ciclos, repitiendo el último
    valor conocido para los ciclos que faltan."""
    por_ciclo = {int(f["ciclo"]): _num(f[medida]) for f in filas}
    serie, ultimo = [], float("nan")
    for c in range(ciclos + 1):
        if c in por_ciclo:
            ultimo = por_ciclo[c]
        serie.append(ultimo)
    return serie


def analiza_configuracion(config, formato_anterior=False):
    corridas = ejecuciones(config)
    if not corridas:
        return None
    primera = Corrida(corridas[0])
    filas = [_lee_csv(d / "metricas_ciclo.csv") for d in corridas]
    ciclos = max([primera.ciclos_planeados] + [int(f[-1]["ciclo"]) for f in filas])

    if formato_anterior:
        # Formato anterior: agrupamiento, ASPL, diámetro (media y desviación estándar poblacional)
        series = {m: [_serie(f, m, ciclos) for f in filas] for m in ("agrupamiento", "aspl", "diametro")}
        with open(config / "datos-promedio.csv", "w", encoding="utf-8") as f:
            f.write("ciclo,avCl,aslp,dia,std_avCL,std_aspl,std_dia\n")
            for c in range(ciclos + 1):
                vals = [[s[c] for s in series[m]] for m in ("agrupamiento", "aspl", "diametro")]
                medias = [sum(v) / len(v) for v in vals]
                f.write(f"{c}," + ",".join(f"{x:.3f}" for x in medias) + ","
                        + ",".join(f"{np.std(v):.3f}" for v in vals) + "\n")

        # Formato anterior: distribución de grados promedio de la red final
        hists = []
        for d in corridas:
            ultimo = int(_lee_csv(d / "metricas_ciclo.csv")[-1]["ciclo"])
            with open(d / f"hist_test_{ultimo}.txt", encoding="utf-8") as f:
                hists.append([float(l.split("\t")[1]) for l in f if l.strip()])
        maximo = max(len(h) for h in hists)
        with open(config / "datos-promedio_grados.csv", "w", encoding="utf-8") as f:
            f.write("grado,prom_nodos\n")
            for g in range(maximo):
                f.write(f"{g},{sum(h[g] if g < len(h) else 0 for h in hists) / len(hists):.6f}\n")

    # Todas las medidas por ciclo: media e IC 95 %
    with open(config / "metricas-promedio.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["ciclo", "ejecuciones"] + [f"{m}{s}" for m in MEDIDAS for s in ("", "_ic95")])
        for c in range(ciclos + 1):
            fila = [c, len(filas)]
            for m in MEDIDAS:
                fila += [_fmt(x) for x in medidas.media_ic95([_serie(fs, m, ciclos)[c] for fs in filas])]
            w.writerow(fila)

    # Estado final de cada ejecución
    finales = []
    for d, fs in zip(corridas, filas):
        corrida = Corrida(d)
        ult = (fs[1:] or fs)[-ULTIMOS:]   # últimos ciclos, sin la red base
        fila = {"ejecucion": corrida.numero,
                "ciclos_completados": int(fs[-1]["ciclo"]),
                "motivo_fin": corrida.resumen.get("motivo_fin", "")}
        for m in MEDIDAS:
            vals = [_num(x[m]) for x in ult if x[m] != ""]
            fila[m] = sum(vals) / len(vals) if vals else float("nan")
        nav = {r["red"]: r for r in _lee_csv(d / "navegabilidad.csv")}
        for m in NAVEGABILIDAD:
            fila[f"{m}_base"] = _num(nav["base"][m])
            fila[f"{m}_final"] = _num(nav["final"][m])
        finales.append(fila)
    columnas = list(finales[0])
    with open(config / "estado-final.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(columnas)
        for fila in finales:
            w.writerow([_fmt(fila[k]) for k in columnas])
    return primera, finales


def fila_resumen(config, relativa, primera, finales):
    """Una fila de la tabla global estado_final.csv: identificación de la
    configuración y media e IC 95 % del estado final de cada medida."""
    p = primera.parametros
    fila = {"configuracion": relativa,
            "red": p.get("red"), "nodos": primera.nodos,
            "exploracion": p.get("routing"), "p": p.get("p"), "q": p.get("q"),
            "regla": p.get("regla"),
            "umbral_r1": p.get("umbral_r1", 0.5) if p.get("regla") == 1 else None,
            "umbral_enlace": p.get("umbral_enlace", 1.0),
            "long_enlace": p.get("long_enlace"),
            "ejecuciones": len(finales),
            "terminaron_por_diametro_2": sum(1 for x in finales if x["motivo_fin"] == "diametro_2")}
    for m in [k for k in finales[0] if k not in ("ejecucion", "motivo_fin", "nodos")]:
        media, ic = medidas.media_ic95([x[m] for x in finales])
        fila[m], fila[f"{m}_ic95"] = media, ic
    return fila
