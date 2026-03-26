from pathlib import Path

#Configuración de una serie de experimentos de formación de redes
#--------- Directorios para guardar resultados -----------
home_path = Path.home()
BASE_DIR = str(home_path) + "/Documents/Repositorios/ResultadosCN/"
RESULTADOS_DIR = BASE_DIR + "Formacion"
#-------- Red inicial: Anillo ------------------
NODOS_ANILLO=64             # Número de nodos del anillo. Colocar 0 si no se usa anillo
#-------- Red inicial: Malla -------------------
ROWS=8                      # Filas de la malla. Colocar 0 si no se usa malla
COLUMNS=8                   # Columnas de la malla
#-------- Configuración de los experimentos de Reconexión -------------
# Estos parámetros se deben definir como lista aunque contengan un solo valor
RED=["malla","anillo"]  # Tipo de red: "malla", "anillo"
ROUTING=["SHORTEST-PATH","COMPASS-ROUTING","RANDOM-WALK"]               
REGLAS=[1,2,3]
# Divisor de la longitud de enlace dinámico.
# Se recomendan valores que sean potencia de 2, 
# p.e., 1, 2, 4, 8, 16, etc. 
LONG_ENLACES=[1,2,4]             
#--------EJECUCION---------------
CICLOS=5                   # Número de ciclos de reconexión
EJECUCIONES = 4            # Número de ejecuciones por experimento   
#--------EXTRAS------------------
ENLACES_DINAMICOS=2        # Número de enlaces dinámicos por nodo
EXPLORADORES=6             # Número de paquetes exploradores por ciclo
# Divisor del máximo número de conexiones permitidas 
# máximo numero de conexiones permitidas=num_nodos/DIV_CONEXIONES
DIV_CONEXIONES=1            