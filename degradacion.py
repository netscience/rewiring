import subprocess
import os
import shutil
import configFormacion
import configDegradacion
import configPaths
import glob

def copia_archivos_para_degradacion():
    # Copia los archivos de los grafos a la carpeta de degradacion
    for red in configFormacion.RED:
        if red == "anillo":
            nombre_red = "anillo" + str(configFormacion.NODOS_ANILLO)
        elif red == "malla":
            nombre_red = f"malla{configFormacion.ROWS}x{configFormacion.COLUMNS}"
        else:
            print(f" Tipo de red desconocido, saltando: {red}")
            continue   
        for r in configFormacion.REGLAS:
            for ruteo in configFormacion.ROUTING:
                routing = "x"
                if ruteo == "COMPASS-ROUTING":
                    routing = "CR"
                elif ruteo == "RANDOM-WALK":
                    routing = "RW" 
                elif ruteo == "SHORTEST-PATH":
                    routing = "SP"
                else:
                    print(f" Algoritmo de ruteo desconocido, saltando: {ruteo}")
                    continue

                for long_enlace in configFormacion.LONG_ENLACES:
                    for i in range(1, configFormacion.EJECUCIONES + 1):
                        # Ruta donde están los grafos formados
                        ruta_grafo = f"{configPaths.RESULTADOS_DIR}/{nombre_red}/R{r}/{routing}/D{long_enlace}/{i}/"
                        if os.path.exists(ruta_grafo):
                            # Buscar el grafo del último ciclo disponible
                            grafos = glob.glob(ruta_grafo + "graph_test_*.adjlist")
                            ultimo_grafo = max(grafos, key=lambda x: int(os.path.splitext(x)[0][-1]))
                            for tipo_degradacion in configDegradacion.TIPO_DEGRADACION:
                                if tipo_degradacion=="Fallas":
                                    script_degradacion = "failureDegradation.py"
                                elif tipo_degradacion=="Ataques":
                                    script_degradacion = "hubDegradation.py"
                                else:
                                    print(f" Tipo de degradación desconocido, saltando: {tipo_degradacion}")
                                    continue
                                carpeta_resultados = f"{configPaths.DEGRADACION_DIR}/{tipo_degradacion}/{nombre_red}/R{r}/{routing}/D{long_enlace}/{i}/"
                                archivo_destino = f"{carpeta_resultados}{os.path.basename(ultimo_grafo)}"
                                # Crear directorios intermedios si no existen
                                os.makedirs(os.path.dirname(archivo_destino), exist_ok=True)
                                # Copia los scrips de degradación a la carpeta de resultados si no existen
                                shutil.copy2("configDegradacion.py", carpeta_resultados)
                                shutil.copy2(script_degradacion, carpeta_resultados)
                                shutil.copy2(ultimo_grafo, archivo_destino)
                                #print(f"\nCopiando: {ultimo_grafo}")
                                #print(f"\na: {archivo_destino}")
                        else:
                            print(f" Ruta no encontrada, saltando: {ruta_grafo}")
                            continue

def ejecutar_degradacion():
    for red in configFormacion.RED:
        if red == "anillo":
            nombre_red = "anillo" + str(configFormacion.NODOS_ANILLO)
        elif red == "malla":
            nombre_red = f"malla{configFormacion.ROWS}x{configFormacion.COLUMNS}"
        else:
            print(f" Tipo de red desconocido, saltando: {red}")
            continue   
        for r in configFormacion.REGLAS:
            routing = "x"
            for ruteo in configFormacion.ROUTING:
                if ruteo == "COMPASS-ROUTING":
                    routing = "CR"
                elif ruteo == "RANDOM-WALK":
                    routing = "RW" 
                elif ruteo == "SHORTEST-PATH":
                    routing = "SP"
                else:
                    print(f" Algoritmo de ruteo desconocido, saltando: {ruteo}")
                    continue

                for long_enlace in configFormacion.LONG_ENLACES:
                    for i in range(1, configFormacion.EJECUCIONES + 1):
                        # Ejecutar degradación desde carpeta destino
                        for tipo_degradacion in configDegradacion.TIPO_DEGRADACION:
                            # Ruta donde están los grafos formados
                            ruta_grafo = f"{configPaths.DEGRADACION_DIR}/{tipo_degradacion}/{nombre_red}/R{r}/{routing}/D{long_enlace}/{i}/"
                            if os.path.exists(ruta_grafo):
                                # Buscar el archivo del grafo
                                grafos = glob.glob(ruta_grafo + "graph_test_*.adjlist")
                                ultimo_grafo = max(grafos, key=lambda x: int(os.path.splitext(x)[0][-1]))
                                
                                degradation_file = ""
                                carpeta_resultados = f"{configPaths.DEGRADACION_DIR}/{tipo_degradacion}/{nombre_red}/R{r}/{routing}/D{long_enlace}/{i}/"
                                if tipo_degradacion=="Fallas":
                                    degradation_file = "failureDegradation.py"
                                elif tipo_degradacion=="Ataques":
                                    degradation_file = "hubDegradation.py"
                                else:
                                    print(f" Tipo de degradación desconocido, saltando: {tipo_degradacion}")
                                    continue
                                
                                subprocess.run([
                                    "python",
                                    degradation_file,
                                    os.path.basename(ultimo_grafo),
                                    str(carpeta_resultados)
                                ], cwd=carpeta_resultados)
                                
                                print(f"\nEjecutando: python {degradation_file} {os.path.basename(ultimo_grafo)} {carpeta_resultados} en {carpeta_resultados}")
                            else:
                                print(f" Ruta no encontrada, saltando: {ruta_grafo}")
                                continue

# Primero, copiar los archivos necesarios para la degradación
copia_archivos_para_degradacion()
# Ejecutar la degradación en los grafos copiados
ejecutar_degradacion()