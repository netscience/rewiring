
import os
import networkx as nx
import shutil
import config_paths as paths

#print(list(os.walk(ejemplo_dir)))
print(paths.RESULTADOS_DIR)
for nombre_directorio, subdirectorios, ficheros in os.walk(paths.RESULTADOS_DIR):#recorro recursivamente un directorio
	if len(subdirectorios)==0:
		shutil.copy2("config.py", nombre_directorio+"/")
		shutil.copy2("main.py", nombre_directorio+"/")
		shutil.copy2("complexNetwork.py", nombre_directorio+"/")
		shutil.copy2("encaminamiento.py", nombre_directorio+"/")
		shutil.copy2("enlace.py", nombre_directorio+"/")
		shutil.copy2("event.py", nombre_directorio+"/")
		shutil.copy2("extractData.py", nombre_directorio+"/")
		shutil.copy2("model.py", nombre_directorio+"/")
		shutil.copy2("paquete.py", nombre_directorio+"/")
		shutil.copy2("process.py", nombre_directorio+"/")
		shutil.copy2("simulation.py", nombre_directorio+"/")
		shutil.copy2("simulator.py", nombre_directorio+"/")
	else:
		print("Los archivos ya habían sido copiado")
