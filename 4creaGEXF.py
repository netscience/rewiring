
import os
import networkx as nx
import config_paths as paths
import config
import math


#print(list(os.walk(ejemplo_dir)))
def getCoordinatesAnillo(nodeId,nodos):
	#transformacion de coordenadas polares a rectangulares:
	angulo = math.radians((360/nodos)*nodeId)#la función math.radians() convierte los grados sexagesimales en radianes
	x = 10*math.cos(angulo)#se asume que el anillo tiene radio 10
	y = 10*math.sin(angulo)#se asume que el anillo tiene radio 10
	coord = (x,y)
	#print("soy",nodeId,"mis coordenadas son",coord)
	return coord

def getCoordinates(nodeId,nodos,contador):
		"""calculates the coordinates of an node id according to the grid used by the simulation """
		x = (nodeId-1)%nodos
		coord = [x,contador]
		return coord

for nombre_directorio, subdirectorios, ficheros in os.walk(paths.RESULTADOS_DIR	):#recorro recursivamente un directorio
	#Obtiene las coordenas
	coordenadas=[]
	if "malla" in nombre_directorio:
		nodes = config.COLUMNS*config.ROWS
		contador=config.COLUMNS-1
		identificador=1
		for i in range(1,config.COLUMNS+1):
			for j in range(1,config.ROWS+1):
				coordenadas.append(getCoordinates(identificador,config.COLUMNS,contador))
				identificador+=1
			contador-=1
	else:
		nodes = config.NODOS_ANILLO
		for i in range(1,nodes+1):
			coordenadas.append(getCoordinatesAnillo(i,nodes))
	
	x = dict()
	y = dict()
	for i in range(nodes):
		x[i+1] = coordenadas[i][0]
		y[i+1] = coordenadas[i][1]
	ultima=nombre_directorio[len(nombre_directorio)-1]
	penultima=nombre_directorio[len(nombre_directorio)-2]
	ciclo1=""
	lista=["/1","/2","/3","/4","/5","/6","/7","/8","/9","10"]
	if(penultima+ultima in lista):
		if penultima+ultima=="10":
			ultima="10"
		primero=open(nombre_directorio+"/datos-salida_"+ultima+".txt","r")
		lineasPrimero = primero.readlines()
		primero.close()
		ciclo1,AVCL,components,diam,APL,order = lineasPrimero[len(lineasPrimero)-1].split("\t")
		G1 = nx.read_adjlist(nombre_directorio+"/graph_test_"+ciclo1+".adjlist", nodetype=int)
		nx.set_node_attributes(G1, x, "x")
		nx.set_node_attributes(G1, y, "y")
		nx.write_gexf(G1, nombre_directorio+"/graph_test_"+ciclo1+".gexf")
	#for nombre_fichero in ficheros:
		#if(nombre_fichero!="graph_test_"+ciclo1+".graphml" and nombre_fichero!="graph_test_"+ciclo1+".adjlist" and nombre_fichero!="distGradoshist_test_"+ciclo1+".txt.png" and nombre_fichero!="img_graph_test_"+ciclo1+".adjlist.png"):
			#os.remove(nombre_directorio+"/"+nombre_fichero)#elimina el archivo indicado