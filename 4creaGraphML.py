
import os
import networkx as nx

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
		G1 = nx.read_adjlist(nombre_directorio+"\\graph_test_"+ciclo1+".adjlist", nodetype=int)
		nx.write_graphml_lxml(G1, nombre_directorio+"\\graph_test_"+ciclo1+".graphml")
	#for nombre_fichero in ficheros:
		#if(nombre_fichero!="graph_test_"+ciclo1+".graphml" and nombre_fichero!="graph_test_"+ciclo1+".adjlist" and nombre_fichero!="distGradoshist_test_"+ciclo1+".txt.png" and nombre_fichero!="img_graph_test_"+ciclo1+".adjlist.png"):
			#os.remove(nombre_directorio+"\\"+nombre_fichero)#elimina el archivo indicado