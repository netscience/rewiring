"""
Medidas sobre redes. Todas reciben grafos de NetworkX con nodos enteros.

Las distancias se calculan con scipy (búsqueda en anchura en C), de modo que
ASPL, diámetro y navegabilidad son exactos también para 5040 nodos.
"""

import math

import networkx as nx
import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import connected_components, shortest_path


#---Distancias----------------------------------------------------------

class Distancias:
    """Matriz de distancias (en saltos) entre todos los nodos de un grafo, como
    enteros de 16 bits (-1 = inalcanzable). Se calcula por bloques para no
    ocupar memoria de más."""

    def __init__(self, G, bloque=512):
        self.nodos = sorted(G.nodes())
        self.indice = {v: i for i, v in enumerate(self.nodos)}
        n = len(self.nodos)
        A = _adyacencia(G, self.indice)
        self.D = np.empty((n, n), dtype=np.int16)
        for i in range(0, n, bloque):
            filas = shortest_path(A, method="D", unweighted=True, directed=False,
                                  indices=np.arange(i, min(i + bloque, n)))
            filas[np.isinf(filas)] = -1
            self.D[i:i + len(filas)] = filas.astype(np.int16)

    def d(self, u, v):
        return int(self.D[self.indice[u], self.indice[v]])


def _adyacencia(G, indice):
    n = len(indice)
    filas, cols = [], []
    for u, v in G.edges():
        filas += [indice[u], indice[v]]
        cols += [indice[v], indice[u]]
    return csr_matrix((np.ones(len(filas), dtype=np.int8), (filas, cols)), shape=(n, n))


#---Medidas estructurales-------------------------------------------------

def estructurales(G):
    """Agrupamiento medio, componentes, orden, diámetro y ASPL, como extractData.py.
    Si la red no es conexa, el diámetro y el ASPL son los de la componente gigante."""
    avcl = nx.average_clustering(G)
    ncomp = nx.number_connected_components(G)
    orden = G.order()
    H = G if ncomp == 1 else G.subgraph(max(nx.connected_components(G), key=len))
    D = Distancias(H).D.astype(np.int64)
    n = H.order()
    diam = int(D.max())
    aspl = int(D.sum()) / (n * (n - 1)) if n > 1 else 0.0  # mismo cálculo que networkx
    return {"agrupamiento": avcl, "componentes": ncomp, "nodos": orden,
            "diametro": diam, "aspl": aspl, "frac_gigante": n / orden if orden else 0.0}


def grados(G):
    return np.array([d for _, d in G.degree()], dtype=float)


def gini(valores):
    """Índice de Gini de valores no negativos: 0 si todos son iguales.
    En la distribución de grados de una estrella de n nodos vale (n - 2) / (2n),
    que tiende a 0.5: en una red conexa cada nodo tiene grado al menos 1 y cada
    enlace suma grado en sus dos extremos, así que no se acerca a 1."""
    x = np.sort(np.asarray(valores, dtype=float))
    n = len(x)
    if n == 0 or x.sum() == 0:
        return 0.0
    i = np.arange(1, n + 1)
    return float((2 * (i * x).sum()) / (n * x.sum()) - (n + 1) / n)


def de_grados(G):
    k = grados(G)
    media = k.mean() if len(k) else 0.0
    return {"grado_medio": media, "grado_max": int(k.max()) if len(k) else 0,
            "cv_grado": (k.std() / media) if media else 0.0,
            "gini_grado": gini(k)}


def asortatividad(G):
    k = grados(G)
    if len(k) == 0 or k.min() == k.max():
        return float("nan")  # red regular: no está definida
    with np.errstate(all="ignore"):
        return float(nx.degree_assortativity_coefficient(G))


def ks_grados(G1, G2):
    """Distancia de Kolmogorov-Smirnov entre las distribuciones de grado de dos redes."""
    a, b = np.sort(grados(G1)), np.sort(grados(G2))
    valores = np.union1d(a, b)
    Fa = np.searchsorted(a, valores, side="right") / len(a)
    Fb = np.searchsorted(b, valores, side="right") / len(b)
    return float(np.abs(Fa - Fb).max())


def enlaces_dinamicos(G, base):
    """Aristas de G que no están en la red base (formato anterior)."""
    return {frozenset(e) for e in G.edges() if not base.has_edge(*e)}


def frac_cambio(actual, anterior):
    """Fracción de enlaces dinámicos que cambió respecto al ciclo anterior.
    Con el formato actual, `actual` y `anterior` son {(nodo, enlace): conectado}
    y cuenta los enlaces que se conectaron o cambiaron de destino; con el
    anterior, son conjuntos de aristas dinámicas."""
    if isinstance(actual, dict):
        if not actual:
            return 0.0
        cambiaron = sum(1 for k, v in actual.items() if anterior.get(k) != v)
        return cambiaron / len(actual)
    if not actual:
        return 0.0
    return len(actual - anterior) / len(actual)


#---Navegabilidad---------------------------------------------------------

def navegabilidad(G, dist_base, pares, rng):
    """Ruteo greedy en G guiado por la distancia en saltos de la red base: desde
    cada nodo se avanza al vecino más cercano al destino; falla si ningún vecino
    está más cerca.

    Regresa éxito (fracción de pares que llegan), pasos medios de los que llegan
    y estiramiento medio (pasos / distancia más corta en G)."""
    nodos = dist_base.nodos
    idx = dist_base.indice
    D = dist_base.D
    vecinos = {u: np.array([idx[v] for v in G.neighbors(u)], dtype=np.int64) for u in nodos}
    n = len(nodos)
    if n < 2:
        return {"pares": 0, "exito": float("nan"), "pasos_medios": float("nan"), "estiramiento": float("nan")}
    origenes = rng.integers(0, n, size=pares)
    destinos = (origenes + rng.integers(1, n, size=pares)) % n   # destino distinto del origen
    # distancias más cortas en G desde cada origen
    A = _adyacencia(G, idx)
    unicos, inversa = np.unique(origenes, return_inverse=True)
    corta = shortest_path(A, method="D", unweighted=True, directed=False, indices=unicos)
    exitos, pasos, estir = 0, [], []
    for k in range(pares):
        s, t = origenes[k], destinos[k]
        u, h = s, 0
        while u != t:
            vs = vecinos[nodos[u]]
            if len(vs) == 0:
                break
            dv = D[vs, t]
            j = int(np.argmin(dv))
            if dv[j] >= D[u, t]:
                break   # mínimo local: ningún vecino está más cerca
            u, h = int(vs[j]), h + 1
        if u == t:
            exitos += 1
            pasos.append(h)
            estir.append(h / corta[inversa[k], t])
    return {"pares": pares, "exito": exitos / pares,
            "pasos_medios": float(np.mean(pasos)) if pasos else float("nan"),
            "estiramiento": float(np.mean(estir)) if estir else float("nan")}


#---Resúmenes sobre ejecuciones------------------------------------------

def media_ic95(valores):
    """Media e intervalo de confianza al 95 % (semiancho, t de Student)."""
    x = np.array([v for v in valores if v is not None and not (isinstance(v, float) and math.isnan(v))], dtype=float)
    if len(x) == 0:
        return float("nan"), float("nan")
    if len(x) == 1:
        return float(x[0]), float("nan")
    from scipy.stats import t
    return float(x.mean()), float(t.ppf(0.975, len(x) - 1) * x.std(ddof=1) / math.sqrt(len(x)))
