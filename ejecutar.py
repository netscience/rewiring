"""
Ejecuta una corrida del simulador.

Uso:
    python ejecutar.py parametros.json [carpeta]

Lee los parámetros de la corrida (ver parametros.py) y escribe en `carpeta`
(por omisión, la carpeta donde está parametros.json):
    graph.adjlist             red inicial
    semilla.txt               semilla usada (vacío si la corrida no es reproducible)
    metricas_rendimiento.csv  tiempo de ejecución y conteo de mensajes por tipo

Los eventos de conexión y reconexión se imprimen en la salida estándar, una
línea por evento ("r fuente desconecta conecta ciclo" o "c fuente -1 conecta ciclo");
formacion.py la redirige a salida_<n>.txt.

El simulador se puede llamar desde otro programa con simular(parametros, carpeta).
"""

import random
import sys
import time
from pathlib import Path

import networkx as nx
import numpy as np

import redes
from complexNetwork import ComplexNetwork
from event import Event
from paquete import Paquete
from parametros import Parametros
from simulation import Simulation

TIPOS_EVENTO = [
    "PIF-EXPLORACION",
    "PACKAGE",
    "ACK",
    "PIF-NEGOCIACION",
    "SOLICITUD-CONEXION",
    "ACEPTO-CONEXION",
    "DESCONEXION",
    "DESCONEXION-RECIBIDA",
    "RECHAZO-CONEXION",
    "PIF-CONEXION",
]


class Corrida:
    """Estado global de una corrida, compartido por todos los nodos.

    Los nodos (ComplexNetwork) y el encaminamiento consultan aquí la red
    (geometría), el grafo NetworkX actual, el número de ciclos, el número de
    nodos y la longitud máxima de los enlaces dinámicos."""

    def __init__(self, parametros):
        self.__parametros = parametros
        self.__ciclos = parametros.ciclos     # Número de ciclos de simulación
        self.__red = None                     # Objeto de redes.py con la geometría de la red (coordenadas, distancia)
        self.__graph = None                   # Grafo NetworkX sobre el que se desarrolla la simulación
        self.__coordinador = 1                # Identificador del nodo coordinador de la simulación
        self.__nodosTotales = -1              # Número de nodos total del grafo
        self.__tamEnlace = None               # Longitud máxima de un enlace dinámico

    #---CREACION DE LA RED----------------

    def crearRed(self, carpeta="."):
        """Construye la red indicada en los parámetros usando redes.py y la
        guarda en carpeta/graph.adjlist."""
        par = self.__parametros
        self.__red = redes.obtener_red(par.red, par.cfg_red())
        self.__graph = self.__red.construir()
        self.__tamEnlace = self.__red.longitud_maxima() / par.long_enlace
        self.__nodosTotales = self.__graph.number_of_nodes()
        nx.write_adjlist(self.__graph, str(Path(carpeta) / "graph.adjlist"))

    #---GETTERS------------------

    @property
    def parametros(self):
        return self.__parametros

    @property
    def red(self):
        return self.__red

    @property
    def ciclos(self):
        return self.__ciclos

    @property
    def tamEnlace(self):
        return self.__tamEnlace

    @property
    def graph(self):
        return self.__graph

    @property
    def coordinador(self):
        return self.__coordinador

    @property
    def nodosTotales(self):
        return self.__nodosTotales


def fija_semilla(semilla):
    """Fija la semilla de los generadores aleatorios, si se indicó una."""
    if semilla is not None:
        random.seed(int(semilla))     # encaminamiento, complexNetwork
        np.random.seed(int(semilla))  # reglas (np.random.choice)


def simular(par, carpeta="."):
    """Corre una simulación con los parámetros `par` y escribe sus archivos en
    `carpeta`. Regresa un diccionario con el tiempo y los conteos de mensajes."""
    carpeta = Path(carpeta)
    carpeta.mkdir(parents=True, exist_ok=True)
    # La semilla se fija antes de cualquier decisión aleatoria
    fija_semilla(par.semilla)

    corrida = Corrida(par)
    corrida.crearRed(carpeta)

    experimento = Simulation(sys.maxsize, corrida)
    experimento.readAdjacencyListNetworkX()
    # Se asocia una pareja proceso/modelo con cada nodo de la gráfica
    for i in range(1, len(experimento.graph) + 1):
        m = ComplexNetwork(corrida,
                           par.enlaces_dinamicos,                   # enlaces dinámicos del nodo
                           corrida.nodosTotales / par.div_conexiones,  # conexiones soportadas por el nodo
                           par.exploradores,                        # paquetes exploradores por ciclo
                           par.regla,                               # regla de reconexión
                           par.routing,                             # algoritmo de exploración
                           par.p, par.q,                            # Node2Vec
                           par.alpha, par.vector_popularidad, par.vector_distancia)  # R4
        experimento.setModel(m, i)

    # Evento semilla: el coordinador arranca un PIF para la fase de EXPLORACION
    paquete = Paquete(0, 0)
    paquete.diametro = nx.diameter(corrida.graph)
    experimento.init(Event("PIF-EXPLORACION", 0.0, corrida.coordinador, corrida.coordinador, paquete))

    inicio = time.perf_counter()
    experimento.run()
    tiempo = time.perf_counter() - inicio

    conteos = experimento.engine.event_counts
    metricas = {"Tiempo_Ejecucion_Segundos": tiempo,
                "Mensajes_Intercambiados": experimento.engine.total_events}
    metricas.update({t: conteos.get(t, 0) for t in TIPOS_EVENTO})

    # Se registra la semilla usada, para poder reproducir la corrida
    with open(carpeta / "semilla.txt", "w", encoding="utf-8") as f:
        f.write(("" if par.semilla is None else str(par.semilla)) + "\n")
    with open(carpeta / "metricas_rendimiento.csv", "w", encoding="utf-8") as f:
        f.write(",".join(metricas) + "\n")
        f.write(",".join([f"{tiempo:.6f}"] + [str(v) for v in list(metricas.values())[1:]]) + "\n")
    return metricas


if __name__ == "__main__":
    if len(sys.argv) not in (2, 3):
        print(__doc__)
        raise SystemExit(1)
    archivo = Path(sys.argv[1])
    carpeta = Path(sys.argv[2]) if len(sys.argv) == 3 else archivo.parent
    simular(Parametros.leer(archivo), carpeta)
