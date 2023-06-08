
import os
import networkx as nx
import sys
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import math

#este archivo crea todos los archivos de las imagenes png
def creaHistogramaDistGrados(nombre,nodos,ruta,file):
	f=open(nombre)
	lines=f.readlines()
	x=[]
	y=[]
	for line in lines:
		separada=line.split()
		x.append(int(separada[0]))
		y.append(float(int(separada[1])/int(nodos)))
	plt.figure()
	plt.plot(x,y)
	plt.ylabel('Frecuencia')
	plt.xlabel('Grado')
	plt.title('Distribucion de grados')
	plt.savefig(ruta+"\\distGrados"+file+".png", dpi=200)

def getCoordinates(nodeId,nodos,contador):
		"""calculates the coordinates of an node id according to the grid used by the simulation """
		x = (nodeId-1)%nodos
		coord = [x,contador]
		return coord

def draw_graph_grid(graphFile,nodes,ruta,file):
	# Read graph in adjlist format and the position of the nodes in a grid is calculated
	G = nx.read_adjlist(graphFile, comments='#', nodetype=int)
	coordenadas=[]
	nodos=int(nodes)*int(nodes)
	contador=int(nodes)-1
	identificador=1
	for i in range(1,int(nodes)+1):
		for j in range(1,int(nodes)+1):
			coordenadas.append(getCoordinates(identificador,int(nodes),contador))
			identificador+=1
		contador-=1
	posicion = dict(zip(sorted(G),coordenadas))  #Association of positions to nodes
	for key in posicion:
		nt = (float(posicion[key][0]*10), float(posicion[key][1] * 10))
		posicion[key]= nt
	fig = plt.figure(num = None, figsize = (10.5,11), dpi = 200)
	ax = plt.subplot()
	ax.axis('off')
	color = [float(G.degree(v)) for v in G]
	size = [(float(G.degree(v))) for v in G.nodes()]
	#Graficamos nodos y aristas ,with_labels=False
	nodes = nx.draw_networkx_nodes(G,posicion,node_color=color,alpha=0.9,node_size=size,cmap='rainbow',linewidths=0.3,ax=ax)
	nx.draw_networkx_edges(G,posicion,alpha=0.4,width=0.4,edge_color='#585d5f')
	nodes.set_edgecolor('#686868')
	#nx.draw_networkx_labels(G, pos=posicion,font_size=5)# draw node labels/names
	cut = 1.00
	xmax = cut * max(xx for xx, yy in posicion.values())
	ymax = cut * max(yy for xx, yy in posicion.values())
	ax.set_xlim(-5.00, xmax+5.00)
	ax.set_ylim(-5.00, ymax+5.00)
	divider = make_axes_locatable(ax)
	cax = divider.append_axes("right", size="3%", pad=0.1)
	clb = plt.colorbar(nodes,cax=cax)
	clb.set_label("Grado",size=12)
	clb.ax.tick_params(labelsize=12)
	plt.savefig(ruta+"\\img_"+file+".png", dpi=50)

def getCoordinatesAnillo(nodeId,nodos):
	#transformacion de coordenadas polares a rectangulares:
	angulo = math.radians((360/nodos)*nodeId)#la función math.radians() convierte los grados sexagesimales en radianes
	x = 10*math.cos(angulo)#se asume que el anillo tiene radio 10
	y = 10*math.sin(angulo)#se asume que el anillo tiene radio 10
	coord = (x,y)
	#print("soy",nodeId,"mis coordenadas son",coord)
	return coord

def draw_graph_ring(graphFile,nodes,ruta,file):
	# Read graph in adjlist format and the position of the nodes in a ring is calculated
	G = nx.read_adjlist(graphFile, comments='#', nodetype=int)
	coordenadas=[]
	nodos=int(nodes)
	for i in range(1,nodos+1):
		coordenadas.append(getCoordinatesAnillo(i,nodos))
	posicion = dict(zip(sorted(G),coordenadas))  #Association of positions to nodes
	fig = plt.figure(num = None, figsize = (30,30), dpi = 200)
	ax = plt.subplot()
	ax.axis('off')
	color = [float(G.degree(v)) for v in G]
	size = [float(G.degree(v)) for v in G.nodes()]
	#Graficamos nodos y aristas ,with_labels=False
	nodes = nx.draw_networkx_nodes(G,posicion,node_color=color,alpha=0.9,node_size=size,cmap='rainbow',linewidths=0.3,ax=ax)
	nx.draw_networkx_edges(G,posicion,alpha=0.4,width=0.4,edge_color='#585d5f')
	nodes.set_edgecolor('#686868')
	#nx.draw_networkx_labels(G, pos=posicion,font_size=5)# draw node labels/names
	cut = 1.00
	xmax = cut * max(xx for xx, yy in posicion.values())
	ymax = cut * max(yy for xx, yy in posicion.values())
	ax.set_xlim(-10.1, xmax+0.5)
	ax.set_ylim(-10.1, ymax+0.5)
	divider = make_axes_locatable(ax)
	cax = divider.append_axes("right", size="3%", pad=0.1)
	clb = plt.colorbar(nodes,cax=cax)
	clb.set_label("Grado",size=12)
	clb.ax.tick_params(labelsize=12)
	plt.savefig(ruta+"\\img_"+file+".png", dpi=50)

ejemplo_dir = 'C:\\Users\\VG\\Documents\\Formación'#este es el directorio que recorrere recursivamente
#print(list(os.walk(ejemplo_dir)))
for nombre_directorio, subdirectorios, ficheros in os.walk(ejemplo_dir):#recorro recursivamente un directorio
	ultima=nombre_directorio[len(nombre_directorio)-1]
	penultima=nombre_directorio[len(nombre_directorio)-2]
	ciclo1=""
	lista=["\\1","\\2","\\3","\\4","\\5","\\6","\\7","\\8","\\9","10"]
	if(penultima+ultima in lista):
		if penultima+ultima=="10":
			ultima="10"
		primero=open(nombre_directorio+"\\datos-salida_"+ultima+".txt","r")
		lineasPrimero = primero.readlines()
		primero.close()
		ciclo1,AVCL,components,diam,APL,order = lineasPrimero[len(lineasPrimero)-1].split("\t")
		if "malla" in nombre_directorio:
			draw_graph_grid(nombre_directorio+"\\graph_test_"+ciclo1+".adjlist",50,nombre_directorio,"graph_test_"+ciclo1+".adjlist")
			plt.close()
			creaHistogramaDistGrados(nombre_directorio+"\\hist_test_"+ciclo1+".txt",2500,nombre_directorio,"hist_test_"+ciclo1+".txt")
			plt.close()
		else:
			draw_graph_ring(nombre_directorio+"\\graph_test_"+ciclo1+".adjlist",1500,nombre_directorio,"graph_test_"+ciclo1+".adjlist")
			plt.close()
			creaHistogramaDistGrados(nombre_directorio+"\\hist_test_"+ciclo1+".txt",1500,nombre_directorio,"hist_test_"+ciclo1+".txt")
			plt.close()