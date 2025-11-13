import subprocess
from pathlib import Path
import os
import shutil
import configFormacion
import configPaths
# Ruta base actual (asegúrate de estar en ResultadosCN1 al ejecutar)
BASE_DIR = Path.cwd()
PYTHON_EXEC = "python"  # Si tu entorno ya responde a 'python'


def generar_script_constantes(nombre_archivo, long_enlace, regla,tipo_red, ruteo):
    constantes = {
        #--------ANILLO------------------
        # Número de nodos del anillo. Colocar 0 si no se usa anillo
        "NODOS_ANILLO":configFormacion.NODOS_ANILLO, 
        #--------MALLA-------------------
        # Filas de la malla. Colocar 0 si no se usa malla
        "ROWS":configFormacion.ROWS,
        # Columnas de la malla                  
        "COLUMNS":configFormacion.COLUMNS,           
        #--------FORMACION-------------
        # Topología sobre la que se desarrollará la simulación: 1 -> "malla" o 3->"anillo"
        "RED":tipo_red,                           
        # Algoritmo de encaminamiento: "CR", "RW", "SP"
        "ROUTING":ruteo, 
        "REGLA":regla,
        # Divisor de la longitud de enlace dinámico: 1, 2, 4, 8, 16, 32 
        "LONG_ENLACE":long_enlace,        
        #--------EJECUCION---------------
        # Número de ciclos de formación
        "CICLOS":configFormacion.CICLOS,                    
        #--------EXTRAS------------------
        # Número de enlaces dinámicos por nodo
        "ENLACES_DINAMICOS":configFormacion.ENLACES_DINAMICOS,       
        # Número de experimentos a realizar
        "EXPLORADORES":configFormacion.EXPLORADORES,
        # Divisor (con respecto al número de nodos, num_nodos/DIV_CONEXIONES) del máximo número de conexiones permitidas
        "DIV_CONEXIONES":configFormacion.DIV_CONEXIONES         
    }

    with open(nombre_archivo, 'w') as f:
        f.write("# Archivo de constantes generado automáticamente\n\n")
        for nombre, valor in constantes.items():
            if isinstance(valor, str):
                f.write(f'{nombre} = "{valor}"\n')
            else:
                f.write(f"{nombre} = {valor}\n")
    print(f"Archivo '{nombre_archivo}' generado con {len(constantes)} constantes.")


for red in configFormacion.RED:
    if red == "anillo":
        nombre_red = "anillo" + str(configFormacion.NODOS_ANILLO)
        tipo_red = 3
    elif red == "malla":
        nombre_red = f"malla{configFormacion.ROWS}x{configFormacion.COLUMNS}"
        tipo_red = 1    
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
                ruta = f"{configPaths.RESULTADOS_DIR}/{nombre_red}/R{r}/{routing}/D{long_enlace}"
                print(f"\n Explorando: {ruta}")

                if not os.path.exists(ruta):
                    print(f" Ruta no encontrada, saltando: {ruta}")
                    continue
                
                # Crea constantes.py en la ruta
                generar_script_constantes(str(ruta)+"/config.py", long_enlace, r, tipo_red,ruteo)

                for x in range(1, configFormacion.EJECUCIONES + 1):
                    hoja = f"{ruta}/{x}"
                    os.makedirs(hoja, exist_ok=True)

                    print(f"\n Simulación {x} en: {hoja}")

                    salida_txt = f"{hoja}/salida_{x}.txt"
                    #Creo el archivo log
                    log_file = f"{hoja}/log_{x}.txt"
                    with open(log_file, "w", encoding="utf-8") as logfile:
                        logfile.write(f"Log de la ejecución {x} en {ruta}\n")
                    # Ejecuta main.py desde la carpeta CR
                    subprocess.run([PYTHON_EXEC, "main.py", log_file], cwd=ruta, stdout=open(salida_txt, "w"))

                    # Copia archivos auxiliares
                    for archivo in ["extractData.py", "graph.adjlist"]:
                        src = f"{ruta}/{archivo}"
                        dest = f"{hoja}/{archivo}"
                        if os.path.exists(src):
                            shutil.copy(src, dest)
                        else:
                            print(f" No se encontró: {archivo} en {ruta}")

                    # Ejecuta extractData.py desde la hoja
                    if os.path.exists(hoja+"/extractData.py"):
                        print(" Extrayendo datos...")
                        subprocess.run([PYTHON_EXEC, "extractData.py", f"salida_{x}.txt", "test"], cwd=hoja)
                    else:
                        print(" No se puede extraer: falta extractData.py")
