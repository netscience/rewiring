"""
Lectura de los resultados de una corrida y reconstrucción de la red de cada ciclo.

Formato actual (simulador/salida.py): parametros.json, graph.adjlist, nodos.csv,
enlaces.csv, mensajes.csv, resumen.json.

Formato anterior: salida_<n>.txt con los eventos de conexión ("c fuente -1
conecta ciclo") y reconexión ("r fuente desconecta conecta ciclo"), graph.adjlist
y config.py en la carpeta de la configuración.
"""

import csv
import json
import math
from pathlib import Path

import networkx as nx


def es_carpeta_configuracion(carpeta, subcarpetas):
    """Una carpeta de configuración tiene como subcarpetas las ejecuciones 1, 2, ..., n."""
    if not subcarpetas or not all(d.isdigit() for d in subcarpetas):
        return False
    if sorted(int(d) for d in subcarpetas) != list(range(1, len(subcarpetas) + 1)):
        return False
    return all(es_corrida(Path(carpeta) / d) for d in subcarpetas)


def es_corrida(carpeta):
    carpeta = Path(carpeta)
    return (carpeta / "enlaces.csv").exists() or (carpeta / f"salida_{carpeta.name}.txt").exists()


def configuraciones(resultados):
    """Carpetas de configuración bajo `resultados`, en orden."""
    import os
    encontradas = []
    for raiz, dirs, _ in os.walk(resultados):
        dirs[:] = sorted(d for d in dirs if d != "__pycache__")
        if es_carpeta_configuracion(raiz, dirs):
            encontradas.append(Path(raiz))
            dirs[:] = []
    return encontradas


def ejecuciones(config):
    """Carpetas de las ejecuciones de una configuración, en orden 1..n."""
    config = Path(config)
    return sorted((d for d in config.iterdir() if d.is_dir() and d.name.isdigit()), key=lambda d: int(d.name))


#---Parámetros-------------------------------------------------------

def _config_anterior(config_py):
    """Lee un config.py del formato anterior como diccionario de constantes."""
    datos = {}
    exec(compile(Path(config_py).read_text(encoding="utf-8"), str(config_py), "exec"), {}, datos)
    red = datos.get("RED")
    red = {1: "malla", 3: "anillo"}.get(red, red)
    geometria = {"malla": ("ROWS", "COLUMNS"), "anillo": ("NODOS_ANILLO",)}.get(red, ())
    return {
        "red": red,
        "geometria": {k: datos[k] for k in geometria if k in datos},
        "routing": datos.get("ROUTING"),
        "regla": datos.get("REGLA"),
        "long_enlace": datos.get("LONG_ENLACE"),
        "ciclos": datos.get("CICLOS"),
        "enlaces_dinamicos": datos.get("ENLACES_DINAMICOS"),
        "exploradores": datos.get("EXPLORADORES"),
        "p": datos.get("P", 0),
        "q": datos.get("Q", 0),
    }


def lee_parametros(carpeta):
    """Parámetros de una corrida: parametros.json, o el config.py de su configuración."""
    carpeta = Path(carpeta)
    if (carpeta / "parametros.json").exists():
        return json.loads((carpeta / "parametros.json").read_text(encoding="utf-8"))
    for c in (carpeta / "config.py", carpeta.parent / "config.py"):
        if c.exists():
            return _config_anterior(c)
    raise FileNotFoundError(f"No hay parametros.json ni config.py para {carpeta}")


#---Corrida----------------------------------------------------------

class Corrida:
    """Resultados de una corrida: parámetros, red base, coordenadas y la red de cada ciclo."""

    def __init__(self, carpeta):
        self.carpeta = Path(carpeta)
        self.numero = int(self.carpeta.name)
        self.parametros = lee_parametros(self.carpeta)
        self.base = nx.read_adjlist(self.carpeta / "graph.adjlist", nodetype=int)
        self.formato_anterior = not (self.carpeta / "enlaces.csv").exists()
        self.resumen = {}
        if (self.carpeta / "resumen.json").exists():
            self.resumen = json.loads((self.carpeta / "resumen.json").read_text(encoding="utf-8"))
        self._coordenadas = None

    @property
    def nodos(self):
        return self.base.number_of_nodes()

    @property
    def ciclos_planeados(self):
        return int(self.parametros.get("ciclos") or 0)

    #---Coordenadas---

    def coordenadas(self):
        """{nodo: (x, y)} desde nodos.csv; para el formato anterior se calculan
        como en el simulador (malla y anillo). None si no se conocen."""
        if self._coordenadas is None:
            archivo = self.carpeta / "nodos.csv"
            if archivo.exists():
                with open(archivo, newline="", encoding="utf-8") as f:
                    self._coordenadas = {int(r["nodo"]): (float(r["x"]), float(r["y"])) for r in csv.DictReader(f)}
            else:
                self._coordenadas = _coordenadas_anteriores(self.parametros, sorted(self.base.nodes()))
        return self._coordenadas

    #---Red de cada ciclo---

    def redes(self):
        """Genera (ciclo, G, dinamicos) para cada ciclo, empezando por la red base
        (ciclo 0). `dinamicos` es la lista de (nodo, enlace, conectado) del ciclo,
        o None en el formato anterior (no registra qué enlace es cuál)."""
        if self.formato_anterior:
            yield from self._redes_por_eventos()
        else:
            yield from self._redes_por_enlaces()

    def _redes_por_enlaces(self):
        por_ciclo = {}
        with open(self.carpeta / "enlaces.csv", newline="", encoding="utf-8") as f:
            for r in csv.DictReader(f):
                por_ciclo.setdefault(int(r["ciclo"]), []).append((int(r["nodo"]), int(r["enlace"]), int(r["conectado"])))
        ultimo = self.resumen.get("ciclos_completados", max(por_ciclo, default=0))
        yield 0, self.base.copy(), []
        for c in range(1, ultimo + 1):
            G = self.base.copy()
            dinamicos = por_ciclo.get(c, [])
            G.add_edges_from((u, v) for u, _, v in dinamicos)
            yield c, G, dinamicos

    def _redes_por_eventos(self):
        """Reconstrucción del formato anterior, igual que extractData.py: la red de
        un ciclo es la base con todos los eventos hasta ese ciclo."""
        archivo = self.carpeta / f"salida_{self.numero}.txt"
        G = self.base.copy()
        anterior = "0"
        with open(archivo, encoding="utf-8") as f:
            for linea in f:
                partes = linea.split()
                if len(partes) != 5:
                    continue
                accion, fuente, desconecta, conecta, ciclo = partes
                if ciclo != anterior:
                    yield int(anterior), G.copy(), None
                anterior = ciclo
                if accion == "r":
                    G.remove_edge(int(fuente), int(desconecta))
                G.add_edge(int(fuente), int(conecta))
        yield int(anterior), G.copy(), None

    #---Mensajes---

    def mensajes(self):
        """{ciclo: {tipo: mensajes}} desde mensajes.csv ({} en el formato anterior)."""
        archivo = self.carpeta / "mensajes.csv"
        datos = {}
        if archivo.exists():
            with open(archivo, newline="", encoding="utf-8") as f:
                for r in csv.DictReader(f):
                    datos.setdefault(int(r["ciclo"]), {})[r["tipo"]] = int(r["mensajes"])
        return datos


def _coordenadas_anteriores(parametros, nodos):
    red, g = parametros.get("red"), parametros.get("geometria", {})
    if red == "malla" and "COLUMNS" in g:
        c = g["COLUMNS"]
        return {i: (float((i - 1) % c), float((i - 1) // c)) for i in nodos}
    if red == "anillo" and "NODOS_ANILLO" in g:
        n = g["NODOS_ANILLO"]
        return {i: (10 * math.cos(math.radians((360 / n) * i)), 10 * math.sin(math.radians((360 / n) * i))) for i in nodos}
    return None
