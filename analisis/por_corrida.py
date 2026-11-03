"""
Análisis de una corrida: reconstruye la red de cada ciclo y escribe, en la
carpeta de la corrida,

  metricas_ciclo.csv       una fila por ciclo con todas las medidas (ver COLUMNAS)
  navegabilidad.csv        ruteo greedy por la distancia de la red base, en la red
                           base y en la red final
  longitudes_enlaces.csv   distribución de longitudes de los enlaces dinámicos de la
                           red final (en saltos de la red base), junto con el número
                           medio de nodos a esa distancia de un nodo cualquiera

y, con formato_anterior (opción --formato-anterior de analizar.py), los
archivos que producían los scripts anteriores:

  datos-salida_<n>.txt     ciclo, agrupamiento, componentes, diámetro, ASPL, orden
  hist_test_<c>.txt        histograma de grados del ciclo c (grado, nodos)
  graph_test_<c>.adjlist   red del ciclo c
"""

import csv
import math
from functools import lru_cache
from pathlib import Path

import numpy as np

from . import medidas
from .lectura import Corrida

# componentes y frac_gigante valen 1: la reconexión nunca quita aristas de la red
# base, así que la red siempre es conexa; se conservan como verificación.
COLUMNAS = ["ciclo", "nodos", "aristas", "agrupamiento", "aspl", "diametro", "componentes",
            "frac_gigante", "asortatividad", "grado_medio", "grado_max", "cv_grado", "gini_grado", "ks_grado",
            "enlaces_dinamicos", "frac_cambio", "longitud_media", "mensajes", "mensajes_exploracion"]

TIPOS_EXPLORACION = ("PACKAGE", "ACK")


@lru_cache(maxsize=4)
def _distancias_base(archivo, firma):
    """Distancias de la red base; se reutilizan entre corridas con la misma red."""
    from .lectura import nx
    return medidas.Distancias(nx.read_adjlist(archivo, nodetype=int))


def _fmt(v):
    if v is None or (isinstance(v, float) and math.isnan(v)):
        return ""
    if isinstance(v, float):
        return f"{v:.6f}"
    return str(v)


def escribe_adjlist(G, archivo, comentario=""):
    """Lista de adyacencia en orden canónico (nodos y vecinos ordenados)."""
    with open(archivo, "w", encoding="utf-8") as f:
        if comentario:
            f.write(f"# {comentario}\n")
        for u in sorted(G.nodes()):
            f.write(" ".join([str(u)] + [str(v) for v in sorted(G.neighbors(u)) if v > u]) + "\n")


def analiza_corrida(carpeta, pares=2000, formato_anterior=False, semilla=0):
    carpeta = Path(carpeta)
    corrida = Corrida(carpeta)
    n = corrida.numero
    texto_base = (carpeta / "graph.adjlist").read_bytes()
    dist = _distancias_base(str(carpeta / "graph.adjlist"), hash(texto_base))
    mensajes = corrida.mensajes()

    filas, salida = [], []
    anterior_G, anterior_din = None, None
    G = corrida.base
    for c, G, dinamicos in corrida.redes():
        e = medidas.estructurales(G)
        if dinamicos is not None:
            actual = {(u, k): v for u, k, v in dinamicos}
            aristas_din = [(u, v) for u, _, v in dinamicos]
        else:
            actual = medidas.enlaces_dinamicos(G, corrida.base)
            aristas_din = [tuple(a) for a in actual]
        longitudes = [dist.d(u, v) for u, v in aristas_din]
        m = mensajes.get(c, {})
        fila = {"ciclo": c, "nodos": e["nodos"], "aristas": G.number_of_edges(),
                "agrupamiento": e["agrupamiento"], "aspl": e["aspl"], "diametro": e["diametro"],
                "componentes": e["componentes"], "frac_gigante": e["frac_gigante"],
                "asortatividad": medidas.asortatividad(G), **medidas.de_grados(G),
                "ks_grado": medidas.ks_grados(G, anterior_G) if anterior_G is not None else float("nan"),
                "enlaces_dinamicos": len(aristas_din),
                "frac_cambio": medidas.frac_cambio(actual, anterior_din) if anterior_din is not None else float("nan"),
                "longitud_media": float(np.mean(longitudes)) if longitudes else float("nan"),
                "mensajes": sum(m.values()) if m else None,
                "mensajes_exploracion": sum(m.get(t, 0) for t in TIPOS_EXPLORACION) if m else None}
        filas.append(fila)
        salida.append(e)
        anterior_G, anterior_din = G, actual
        if formato_anterior:
            escribe_adjlist(G, carpeta / f"graph_test_{c}.adjlist", f"red del ciclo {c}")
            with open(carpeta / f"hist_test_{c}.txt", "w", encoding="utf-8") as f:
                for grado, cantidad in enumerate(__import__("networkx").degree_histogram(G)):
                    f.write(f"{grado}\t{cantidad}\n")
        ultimo_c, ultimo_G, ultimas_long = c, G, longitudes

    with open(carpeta / "metricas_ciclo.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(COLUMNAS)
        for fila in filas:
            w.writerow([_fmt(fila[k]) for k in COLUMNAS])

    if formato_anterior:
        with open(carpeta / f"datos-salida_{n}.txt", "w", encoding="utf-8") as f:
            f.write("#cicle\tavCl\tcomponents\tdiam\taspl\torder\n")
            for fila, e in zip(filas, salida):
                f.write(f"{fila['ciclo']}\t{e['agrupamiento']:.6f}\t{e['componentes']}\t"
                        f"{e['diametro']}\t{e['aspl']:.6f}\t{e['nodos']}\n")

    # Navegabilidad en la red base y en la red final, con los mismos pares
    with open(carpeta / "navegabilidad.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["red", "ciclo", "pares", "exito", "pasos_medios", "estiramiento"])
        for nombre, c, H in (("base", 0, corrida.base), ("final", ultimo_c, ultimo_G)):
            r = medidas.navegabilidad(H, dist, pares, np.random.default_rng(semilla))
            w.writerow([nombre, c, r["pares"], _fmt(r["exito"]), _fmt(r["pasos_medios"]), _fmt(r["estiramiento"])])

    # Longitudes de los enlaces dinámicos de la red final y tamaño medio de las esferas
    D = dist.D
    radios = np.arange(0, int(D.max()) + 1)
    esfera = [(D == r).sum() / len(dist.nodos) for r in radios]
    conteo = np.bincount(np.array(ultimas_long, dtype=int), minlength=len(radios)) if ultimas_long else np.zeros(len(radios), int)
    with open(carpeta / "longitudes_enlaces.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["longitud", "enlaces", "esfera_media"])
        for r in radios:
            if r > 0:
                w.writerow([int(r), int(conteo[r]) if r < len(conteo) else 0, f"{esfera[r]:.6f}"])
    return filas
