
import os
import networkx as nx
import shutil
import experimentos

#print(paths.RESULTADOS_DIR)
#print(list(os.walk(paths.RESULTADOS_DIR)))

def crear_arbol_directorios(ruta):
    try:
        os.makedirs(ruta, exist_ok=True)
        print(f"Directorio '{ruta}' creado (o ya existía).")
    except Exception as e:
        print(f"Error al crear directorios: {e}")

# Ejemplo: un árbol como ./proyecto/src/data/output
for red in experimentos.RED:
    if red == "anillo":
        nombre_red = "anillo" + str(experimentos.NODOS_ANILLO)
        tipo_red = 3
    elif red == "malla":
        nombre_red = f"malla{experimentos.ROWS}x{experimentos.COLUMNS}"
        tipo_red = 1    
    else:
        print(f" Tipo de red desconocido, saltando: {red}")
        continue   
    for r in experimentos.REGLAS:
        routing = "x"
        for ruteo in experimentos.ROUTING:
            if ruteo == "COMPASS-ROUTING":
                routing = "CR"
            elif ruteo == "RANDOM-WALK":
                routing = "RW" 
            elif ruteo == "SHORTEST-PATH":
                routing = "SP"
            else:
                print(f" Algoritmo de ruteo desconocido, saltando: {ruteo}")
                continue

            for long_enlace in experimentos.LONG_ENLACES:
                ruta =  f"{experimentos.RESULTADOS_DIR}/{nombre_red}/R{r}/{routing}/D{long_enlace}"
                crear_arbol_directorios(ruta)

# Copio los archivos del experimentos y formacion en la carpeta de resultados
shutil.copy2("experimentos.py", experimentos.BASE_DIR)
shutil.copy2("formacion.py", experimentos.BASE_DIR)

for nombre_directorio, subdirectorios, ficheros in os.walk(experimentos.RESULTADOS_DIR):#recorro recursivamente un directorio

	if len(subdirectorios)==0:
		#shutil.copy2("config.py", nombre_directorio+"/")
		shutil.copy2("main.py", nombre_directorio)
		shutil.copy2("complexNetwork.py", nombre_directorio)
		shutil.copy2("encaminamiento.py", nombre_directorio)
		shutil.copy2("enlace.py", nombre_directorio)
		shutil.copy2("event.py", nombre_directorio)
		shutil.copy2("extractData.py", nombre_directorio)
		shutil.copy2("model.py", nombre_directorio)
		shutil.copy2("paquete.py", nombre_directorio)
		shutil.copy2("process.py", nombre_directorio)
		shutil.copy2("simulation.py", nombre_directorio)
		shutil.copy2("simulator.py", nombre_directorio)
	else:
		print("Los archivos ya habían sido copiado")
