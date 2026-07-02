import os
import shutil
import configuracion

def crear_arbol_directorios(ruta):
    try:
        os.makedirs(ruta, exist_ok=True)
        print(f"Directorio '{ruta}' creado (o ya existía).")
    except Exception as e:
        print(f"Error al crear directorios: {e}")

# Lista de archivos a copiar
archivos_simulador = [
    "complexNetwork.py",
    "encaminamiento.py",
    "enlace.py",
    "event.py",
    "extractData.py",
    "model.py",
    "paquete.py",
    "process.py",
    "simulation.py",
    "simulator.py",
    "main.py",
    "reglas.py"
]

for red in configuracion.RED:
    if red == "anillo":
        nombre_red = "anillo" + str(configuracion.NODOS_ANILLO)
        tipo_red = 3
    elif red == "malla":
        nombre_red = f"malla{configuracion.ROWS}x{configuracion.COLUMNS}"
        tipo_red = 1    
    else:
        print(f" Tipo de red desconocido, saltando: {red}")
        continue   
        
    for r in configuracion.REGLAS:
        routing = "x"
        for ruteo in configuracion.ROUTING:
            if ruteo == "COMPASS-ROUTING":
                routing = "CR"
            elif ruteo == "RANDOM-WALK":
                routing = "RW" 
            elif ruteo == "RW-DEGREE":
                    routing = "RWD"
            elif ruteo == "RW-INVERSE":
                routing = "RWI" 
            elif ruteo == "RW-NODE2VEC":
                routing = "N2V"
            elif ruteo == "SHORTEST-PATH":
                routing = "SP"
            else:
                print(f" Algoritmo de ruteo desconocido, saltando: {ruteo}")
                continue

            for long_enlace in configuracion.LONG_ENLACES:
                if ruteo == "RW-NODE2VEC":
                    for pq in configuracion.PQ_NODE2VEC:
                            p = pq[0]
                            q = pq[1]
                            pstr = str(p).replace('.',"_")
                            qstr = str(q).replace('.',"_")
                            ruta = f"{configuracion.RESULTADOS_DIR}/{nombre_red}/R{r}/{routing}p{pstr}q{qstr}/D{long_enlace}"
                            crear_arbol_directorios(ruta)        
                            # Copiar directamente todos los archivos a esta ruta
                            for archivo in archivos_simulador:
                                if os.path.exists(archivo):
                                    shutil.copy2(archivo, ruta)
                                else:
                                    print(f" Advertencia: no se encontró {archivo} en el directorio raíz.")
                else:
                    ruta = f"{configuracion.RESULTADOS_DIR}/{nombre_red}/R{r}/{routing}/D{long_enlace}"
                    crear_arbol_directorios(ruta)
                
                    # Copiar directamente todos los archivos a esta ruta
                    for archivo in archivos_simulador:
                        if os.path.exists(archivo):
                            shutil.copy2(archivo, ruta)
                        else:
                            print(f" Advertencia: no se encontró {archivo} en el directorio raíz.")

print("Copia de archivos del simulador a todos los directorios completada.")
