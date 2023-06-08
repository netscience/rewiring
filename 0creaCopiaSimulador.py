
import os
import networkx as nx
import shutil

ejemplo_dir = 'C:\\Users\\VG\\Documents\\Formación'#este es el directorio que recorrere recursivamente

#print(list(os.walk(ejemplo_dir)))

for nombre_directorio, subdirectorios, ficheros in os.walk(ejemplo_dir):#recorro recursivamente un directorio
	if len(subdirectorios)==0:
		shutil.copy2("complexNetwork.py", nombre_directorio+"\\")
		shutil.copy2("encaminamiento.py", nombre_directorio+"\\")
		shutil.copy2("enlace.py", nombre_directorio+"\\")
		shutil.copy2("event.py", nombre_directorio+"\\")
		shutil.copy2("extractData.py", nombre_directorio+"\\")
		shutil.copy2("model.py", nombre_directorio+"\\")
		shutil.copy2("paquete.py", nombre_directorio+"\\")
		shutil.copy2("process.py", nombre_directorio+"\\")
		shutil.copy2("simulation.py", nombre_directorio+"\\")
		shutil.copy2("simulator.py", nombre_directorio+"\\")
		if "anillo" in nombre_directorio:
			shutil.copy2("anillo.adjlist", nombre_directorio+"\\")
		else:
			shutil.copy2("malla.adjlist", nombre_directorio+"\\")