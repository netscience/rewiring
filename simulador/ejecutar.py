"""
Ejecuta una corrida del simulador.

Uso (desde la raíz del repositorio, o con ella en PYTHONPATH):
    python -m simulador.ejecutar parametros.json [carpeta]
o también
    python simulador/ejecutar.py parametros.json [carpeta]

Lee los parámetros de la corrida (ver parametros.py) y escribe en `carpeta`
(por omisión, la carpeta donde está parametros.json) la red base, la red de
cada ciclo y los mensajes por ciclo (ver salida.py).

El simulador se puede llamar desde otro programa con simular(parametros, carpeta).
"""

import random
import sys
import time
from pathlib import Path

if not __package__:
    # Corrido como archivo (python simulador/ejecutar.py), o como módulo principal de un proceso
    # hijo de multiprocessing ("spawn", el modo por omisión en macOS y Windows):
    # se importa como paquete para que funcionen las importaciones relativas
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    __package__ = "simulador"
    import simulador  # noqa: F401

import networkx as nx
import numpy as np

from . import redes
from .complexNetwork import ComplexNetwork
from .event import Event
from .paquete import Paquete
from .parametros import Parametros
from .salida import Registro
from .simulation import Simulation

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
        self.modelos = {}                     # id -> ComplexNetwork, para registrar el estado al fin de cada ciclo
        self.motor = None                     # Motor de eventos (conteo de mensajes)
        self.registro = None                  # salida.Registro, o None para no escribir archivos
        self.ciclos_completados = 0
        self.ciclo_diametro_2 = None          # Primer ciclo al final del cual el diámetro es 2

    #---REGISTRO (lo llama el coordinador)---

    def fin_de_ciclo(self, ciclo):
        """El coordinador avisa que terminó el ciclo en toda la red."""
        self.ciclos_completados = ciclo
        if self.registro is not None:
            self.registro.ciclo(ciclo, self.modelos, self.motor.event_counts)

    def diametro_2(self, ciclo):
        if self.ciclo_diametro_2 is None:
            self.ciclo_diametro_2 = ciclo

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
    `carpeta`. Regresa el resumen de la corrida (lo mismo que resumen.json)."""
    carpeta = Path(carpeta)
    carpeta.mkdir(parents=True, exist_ok=True)
    # La semilla se fija antes de cualquier decisión aleatoria
    fija_semilla(par.semilla)

    corrida = Corrida(par)
    corrida.crearRed(carpeta)
    corrida.registro = Registro(carpeta)
    corrida.registro.nodos(corrida.red, sorted(corrida.graph.nodes()))

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
        corrida.modelos[i] = m
    corrida.motor = experimento.engine

    # Evento semilla: el coordinador arranca un PIF para la fase de EXPLORACION
    paquete = Paquete(0, 0)
    paquete.diametro = nx.diameter(corrida.graph)
    experimento.init(Event("PIF-EXPLORACION", 0.0, corrida.coordinador, corrida.coordinador, paquete))

    inicio = time.perf_counter()
    experimento.run()
    tiempo = time.perf_counter() - inicio

    if corrida.ciclos_completados == par.ciclos:
        motivo = "ciclos"
    elif corrida.ciclo_diametro_2 is not None:
        motivo = "diametro_2"
    else:
        motivo = "otro"
    resumen = {"ciclos_completados": corrida.ciclos_completados,
               "motivo_fin": motivo,
               "ciclo_diametro_2": corrida.ciclo_diametro_2,
               "mensajes_totales": experimento.engine.total_events,
               "tiempo_s": round(tiempo, 6),
               "semilla": par.semilla}
    corrida.registro.cerrar(resumen)
    return resumen


if __name__ == "__main__":
    if len(sys.argv) not in (2, 3):
        print(__doc__)
        raise SystemExit(1)
    archivo = Path(sys.argv[1])
    carpeta = Path(sys.argv[2]) if len(sys.argv) == 3 else archivo.parent
    simular(Parametros.leer(archivo), carpeta)
