
import random
import sys
import networkx as nx
import numpy as np
from simulation import Simulation
from complexNetwork import ComplexNetwork
from event import Event
from paquete import Paquete
import config
import redes

class Main:#hereda de la clase object, hay que recordar que en Python todo es un objeto

	def __init__(self):
		self.__ciclos=config.CICLOS      # Número de ciclos de simulación
		self.__grafo=config.RED          # Topología sobre la que se desarrollará la simulación (ver redes.py)
		self.__red = None                # Objeto de redes.py con la geometría de la red (coordenadas, distancia)
		self.__graph = None              # Grafo NetworkX sobre el que se desarrollará la simulación
		self.__coordinador=1             # Identificador del nodo coordinador de la simulación
		self.__nodosTotales=-1           # Número de nodos total del grafo
	
	#---CREACION DE LA RED----------------

	def crearRed(self):
		"""Construye la red indicada en config.RED usando redes.py"""
		self.__red = redes.obtener_red(self.__grafo, config)
		self.__graph = self.__red.construir()
		self.__tamEnlace = self.__red.longitud_maxima() / config.LONG_ENLACE
		self.__nodosTotales = self.__graph.number_of_nodes()
		nx.write_adjlist(self.__graph,"graph.adjlist")

	#---GETTERS y SETTERS------------------

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
	def grafo(self):
		return self.__grafo

	@grafo.setter
	def grafo(self,value):
		self.__grafo=value

	@property
	def graph(self):
		return self.__graph

	@property
	def coordinador(self):
		return self.__coordinador

	@property
	def nodosTotales(self):
		return self.__nodosTotales

	@nodosTotales.setter
	def nodosTotales(self,value):
		self.__nodosTotales=value

def fijaSemilla():
	"""Fija la semilla de la corrida, si se indicó una.

	La semilla se toma del segundo argumento de la línea de comandos
	(python main.py <log> <semilla>) o, si no se da, de config.SEMILLA.
	Sin semilla, la corrida es aleatoria como siempre. Regresa la semilla
	usada o None."""
	semilla = None
	if len(sys.argv) > 2:
		semilla = int(sys.argv[2])
	elif getattr(config, "SEMILLA", None) is not None:
		semilla = int(config.SEMILLA)
	if semilla is not None:
		random.seed(semilla)     # encaminamiento, complexNetwork
		np.random.seed(semilla)  # reglas (np.random.choice)
	return semilla

#---MAIN()-----------------------
if __name__ == "__main__":
	#Se fija la semilla de la corrida (si se indicó) antes de cualquier decisión aleatoria
	semilla = fijaSemilla()
	#Se crea una instancia de la clase Main
	main=Main()
	#Se crea el grafo con el que se trabajará en la simulación (tipos disponibles en redes.py)
	main.crearRed()
	#se muestra el grafo en una imágen:
	#plt.cla()
	#nx.draw_networkx(main.graph)
	#plt.show()
	#Se construye una instancia de la clase Simulation
	experiment = Simulation(sys.maxsize,main)
	experiment.readAdjacencyListNetworkX()
	#Se asocia un pareja proceso/modelo con cada nodo de la gráfica
	for i in range(1,len(experiment.graph)+1):
		#parámetros del constructor de la clase ComplexNetwork
		#el primer parámetro es una referencia al objeto principal de la simulación
		#el segundo parámetro es el número de enlaces dinámicos del nodo
		#el tercer parámetro es el número de conexiones soportadas por el nodo 
		#el cuarto parámetro es el número de paquetes exploradores que enviará el nodo en fase de exploración
		#el quinto parámetro indica el algoritmo de encaminamiento que el nodo ejecutará en la fase de exploración
		#opciones de algoritmo de encaminamiento: "COMPASS-ROUTING", "RANDOM-WALK", "SHORTEST-PATH"
		#el sexto parámetro indica el número de la regla de recableado que el nodo ejecutará en la fase de negociación
		#el septimo parámetro es el número de ejecucipon para ubicar archivo de log donde se registrarán los eventos del nodo
  		#opciones de reglas de recableado: R1=>1, R2=>2, R3=>3
		m = ComplexNetwork(main,config.ENLACES_DINAMICOS,main.nodosTotales/config.DIV_CONEXIONES,config.EXPLORADORES,config.REGLA,config.ROUTING,config.P,config.Q, config.ALPHA, config.VECTOR_POPULARIDAD, config.VECTOR_DISTANCIA)#,sys.argv[1])
		experiment.setModel(m, i)
	#inserta un evento semilla en la agenda y arranca
	#para comenzar la simulacion el coordinador arranca un PIF en donde avisará a todos que hagan su fase de EXPOLRACIÓN
	new_package=Paquete(0,0)
	new_package.diametro=nx.diameter(main.graph)
	seed=Event("PIF-EXPLORACION", 0.0, main.coordinador,main.coordinador,new_package)
	experiment.init(seed)
	
	import time
	from pathlib import Path
	
	start_time = time.perf_counter()
	experiment.run()
	elapsed_time = time.perf_counter() - start_time
	
	total_mensajes = experiment.engine.total_events
	event_counts = experiment.engine.event_counts
	
	event_types = [
		"PIF-EXPLORACION",
		"PACKAGE",
		"ACK",
		"PIF-NEGOCIACION",
		"SOLICITUD-CONEXION",
		"ACEPTO-CONEXION",
		"DESCONEXION",
		"DESCONEXION-RECIBIDA",
		"RECHAZO-CONEXION",
		"PIF-CONEXION"
	]
	
	if len(sys.argv) > 1:
		hoja_dir = Path(sys.argv[1]).parent
	else:
		hoja_dir = Path(".")
		
	#Se registra la semilla usada, para poder reproducir la corrida
	with open(hoja_dir / "semilla.txt", "w", encoding="utf-8") as sf:
		sf.write(("" if semilla is None else str(semilla)) + "\n")

	metrics_file = hoja_dir / "metricas_rendimiento.csv"
	with open(metrics_file, "w", encoding="utf-8") as mf:
		header = ["Tiempo_Ejecucion_Segundos", "Mensajes_Intercambiados"] + event_types
		mf.write(",".join(header) + "\n")
		
		row = [f"{elapsed_time:.6f}", str(total_mensajes)]
		for et in event_types:
			row.append(str(event_counts.get(et, 0)))
		mf.write(",".join(row) + "\n")