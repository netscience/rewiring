"""
Figuras y archivos para Gephi de la red final de una corrida (los de
3creaImagenesPNG.py y 4creaGEXF.py). analizar.py los hace solo para las corridas
indicadas con --figuras:

  img_graph_test_<c>.png        la red final, con los nodos en sus coordenadas,
                                coloreados y escalados por su grado
  distGradoshist_test_<c>.png   distribución de grados de la red final
  graph_test_<c>.gexf           la red final con las coordenadas x, y de cada nodo
                                (para el geoLayout de Gephi)

Las coordenadas se leen de nodos.csv. En la malla el eje y se invierte para que
el nodo 1 quede arriba a la izquierda, como antes.
"""

import matplotlib
matplotlib.use("Agg")   # solo se guardan archivos; no se abren ventanas
import matplotlib.pyplot as plt
import networkx as nx
from mpl_toolkits.axes_grid1 import make_axes_locatable

from .lectura import Corrida

def escala_automatica(nodos):
    """Tamaño de los nodos por unidad de grado: 20 para redes de ~64 nodos, 1 para ~2500."""
    return 20 if nodos <= 200 else (5 if nodos <= 1000 else 1)


def _posiciones(corrida):
    coords = corrida.coordenadas()
    if coords is None:
        return nx.spring_layout(corrida.base, seed=0), False
    if corrida.parametros.get("red") == "malla":
        ymax = max(y for _, y in coords.values())
        coords = {v: (x, ymax - y) for v, (x, y) in coords.items()}
    return coords, True


def _entero_si_puede(v):
    return int(v) if float(v).is_integer() else v


def figuras_corrida(carpeta, escala=None):
    corrida = Corrida(carpeta)
    escala = escala or escala_automatica(corrida.nodos)
    for c, G, _ in corrida.redes():
        pass   # la red final es la última
    pos, geometria = _posiciones(corrida)
    malla = corrida.parametros.get("red") == "malla"

    # Red final
    if malla:
        posicion = {v: (x * 10, y * 10) for v, (x, y) in pos.items()}
        fig = plt.figure(figsize=(10.5, 11), dpi=200)
    else:
        posicion = pos
        fig = plt.figure(figsize=(30, 30), dpi=200)
    ax = plt.subplot()
    ax.axis("off")
    color = [float(G.degree(v)) for v in G]
    tam = [float(G.degree(v)) * escala for v in G]
    nodos = nx.draw_networkx_nodes(G, posicion, node_color=color, alpha=0.9, node_size=tam,
                                   cmap="rainbow", linewidths=0.3, ax=ax)
    nx.draw_networkx_edges(G, posicion, alpha=0.4, width=0.4, edge_color="#585d5f", ax=ax)
    nodos.set_edgecolor("#686868")
    xs = [x for x, _ in posicion.values()]
    ys = [y for _, y in posicion.values()]
    margen = 5.0 if malla else 0.5
    ax.set_xlim(min(xs) - margen, max(xs) + margen)
    ax.set_ylim(min(ys) - margen, max(ys) + margen)
    cax = make_axes_locatable(ax).append_axes("right", size="3%", pad=0.1)
    clb = plt.colorbar(nodos, cax=cax)
    clb.set_label("Grado", size=12)
    clb.ax.tick_params(labelsize=12)
    plt.savefig(carpeta / f"img_graph_test_{c}.png", dpi=50)
    plt.close(fig)

    # Distribución de grados
    hist = nx.degree_histogram(G)
    fig = plt.figure()
    plt.plot(range(len(hist)), [h / corrida.nodos for h in hist])
    plt.ylabel("Frecuencia")
    plt.xlabel("Grado")
    plt.title("Distribucion de grados")
    plt.savefig(carpeta / f"distGradoshist_test_{c}.png", dpi=200)
    plt.close(fig)

    # GEXF con coordenadas
    H = nx.Graph()
    H.add_nodes_from(sorted(G.nodes()))
    H.add_edges_from(sorted(tuple(sorted(e)) for e in G.edges()))
    if geometria:
        nx.set_node_attributes(H, {v: _entero_si_puede(x) for v, (x, _) in pos.items()}, "x")
        nx.set_node_attributes(H, {v: _entero_si_puede(y) for v, (_, y) in pos.items()}, "y")
    nx.write_gexf(H, carpeta / f"graph_test_{c}.gexf")
