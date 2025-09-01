import subprocess
import os
import shutil
import experimentos

def ejecutar_degradacion():
    for red in experimentos.RED:
        if red == "anillo":
            nombre_red = "anillo" + str(experimentos.NODOS_ANILLO)
        elif red == "malla":
            nombre_red = f"malla{experimentos.ROWS}x{experimentos.COLUMNS}"
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
                    # Ruta donde están los grafos formados
                    ruta_formacion = f"{experimentos.RESULTADOS_DIR}/{nombre_red}/R{r}/{routing}/D{long_enlace}"
                    
                    if not os.path.exists(ruta_formacion):
                        print(f" Ruta no encontrada, saltando: {ruta_formacion}")
                        continue
    
                    # Ruta donde se guardarán los resultados de degradación
                    ruta_destino_base = f"{experimentos.DEGRADACION_DIR}/{nombre_red}/R{r}/{routing}/D{long_enlace}"

                    print(f"\nProcesando: {ruta_formacion}")

                    for x in range(1, experimentos.EJECUCIONES + 1):
                        carpeta_origen = ruta_formacion / str(x)
                        carpeta_destino = ruta_destino_base / str(x)
                        carpeta_destino.mkdir(parents=True, exist_ok=True)

                        # Buscar el grafo del último ciclo disponible
                        for ciclo in reversed(range(1, experimentos.CICLOS + 1)):
                            archivo_grafo_origen = carpeta_origen / f"graph_test_{ciclo}.adjlist"
                            if archivo_grafo_origen.exists():
                                print(f"Ejecutando degradación en: {archivo_grafo_origen.name}")
                                print(f"la ruta es {carpeta_destino}")
                                print(f"la ruta total es {carpeta_destino / archivo_grafo_origen.name}")

                                # Copiar grafo y scripts a carpeta destino
                                archivo_grafo_destino = carpeta_destino / archivo_grafo_origen.name
                                if not archivo_grafo_destino.exists():                    
                                    shutil.copy(archivo_grafo_origen, archivo_grafo_destino)
                                #shutil.copy("config.py", carpeta_destino / "config.py")
                                degradation_script =carpeta_destino / experimentos.FILE_DEGRADATION
                                if not degradation_script.exists():
                                    shutil.copy(experimentos.FILE_DEGRADATION, carpeta_destino / experimentos.FILE_DEGRADATION)

                                # Ejecutar degradación desde carpeta destino
                                subprocess.run([
                                    "python",
                                    experimentos.FILE_DEGRADATION,
                                    archivo_grafo_destino.name,
                                    str(carpeta_destino)
                                ], cwd=carpeta_destino)
                                break
                            else:
                                print(f"  No existe: {archivo_grafo_origen.name}")

if __name__ == "__main__":

    ejecutar_degradacion()

