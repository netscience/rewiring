#Configuración de una serie de experimentos de formación y degradación
from pathlib import Path

home_path = Path.home()

BASE_DIR = str(home_path) + "/Documents/Repositorios/ResultadosCN/"

RESULTADOS_DIR = BASE_DIR + "Formación"
DEGRADACION_DIR = BASE_DIR + "Degradación"

#--------ANILLO------------------
NODOS_ANILLO=50             # Número de nodos del anillo. Colocar 0 si no se usa anillo
#--------MALLA-------------------
ROWS=8                      # Filas de la malla. Colocar 0 si no se usa malla
COLUMNS=8                   # Columnas de la malla
#--------FORMACION-------------
RED=["malla","anillo"]  # Tipo de red: "malla", "anillo"
ROUTING=["SHORTEST-PATH","COMPASS-ROUTING","RANDOM-WALK"]                # Algoritmo de encaminamiento: "COMPASS-ROUTING", "RANDOM-WALK", "SHORTEST-PATH"
REGLAS=[1,2,3]              # 1,2,3
LONG_ENLACES=[1,2,3]         # Divisor de la longitud de enlace dinámico: 1, 2, 4, 8, 16, 32 
#--------EJECUCION---------------
CICLOS=4                    # Número de ciclos de recableo
EJECUCIONES = 4            # Número de ejecuciones por experimento   
#--------EXTRAS------------------
ENLACES_DINAMICOS=2         # Número de enlaces dinámicos por nodo
EXPLORADORES=20             # Número de paquetes exploradores por ciclo
DIV_CONEXIONES=1            # Divisor (con respecto al número de nodos, num_nodos/DIV_CONEXIONES) del máximo número de conexiones permitidas
#--------VISUALIZACION-----------
#Parameteros para 3creaImagenesPNG.py
NODE_SCALE = 10     #Usar 1 para orden de anillo=1500 y orde de malla=2500
#-------DEGRADACION------------
SAVE_STEP=4                 #Cada cuántos ataques registra medidas