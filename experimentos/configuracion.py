from pathlib import Path

#Configuración de una serie de experimentos de formación de redes
#--------- Directorios para guardar resultados -----------
home_path = Path.home()
BASE_DIR = str(home_path) + "/Repositorios/ResultadosCN/"
RESULTADOS_DIR = BASE_DIR + "Formacion"
#-------- Red inicial: Anillo ------------------
NODOS_ANILLO=64             # Número de nodos del anillo. Colocar 0 si no se usa anillo
#-------- Red inicial: Malla -------------------
ROWS=8                      # Filas de la malla. Colocar 0 si no se usa malla
COLUMNS=8                   # Columnas de la malla
#-------- Configuración de los experimentos de Reconexión -------------
# Estos parámetros se deben definir como lista aunque contengan un solo valor
RED=["malla","anillo"]  # Tipo de red: "malla", "anillo"
# Algoritmo de ruteo: "SHORTEST-PATH", "COMPASS-ROUTING", "RANDOM-WALK", "RW-DEGREE", "RW-INVERSE", "RW-NODE2VEC"
ROUTING=["SHORTEST-PATH", "COMPASS-ROUTING", "RANDOM-WALK", "RW-DEGREE", "RW-INVERSE", "RW-NODE2VEC"]               
# Parámetros para Node2Vec
PQ_NODE2VEC = [
    (0.25,0.25), (0.25,0.5), (0.25,1), (0.25,2),
    (0.5,0.25), (0.5,0.5), (0.5,1), (0.5,2),
    (1,0.25), (1,0.5), (1,1), (1,2),
    (2,0.25), (2,0.5), (2,1), (2,2)
    ]

# Reglas de reconexión
REGLAS=[1,2,3] #1,2,3,4
# Umbrales de la reconexión (listas, como los demás factores; ver README).
# Ambos se expresan como fracción del número de exploradores del ciclo.
# - UMBRAL_ENLACE (todas las reglas): cuando un nodo ya no tiene enlaces libres,
#   toma su enlace dinámico menos usado en el ciclo y lo reconecta solo si sus
#   usos son menores que UMBRAL_ENLACE * EXPLORADORES. 1 (por omisión) = se
#   reconecta salvo que todos los exploradores lo hayan usado; 0 = nunca se reconecta.
# - UMBRAL_R1 (solo R1): al reconectar, el nodo más visitado solo se acepta si
#   sus visitas en f_n son al menos UMBRAL_R1 * EXPLORADORES. 0.5 (por omisión) =
#   la mitad de los exploradores; 0 = sin umbral. No se aplica al llenar enlaces libres.
# Cada valor distinto del de omisión agrega un sufijo a la carpeta de la regla:
# R1u0_25 (UMBRAL_R1 = 0.25), R3e0_5 (UMBRAL_ENLACE = 0.5), R1u0_25e0_5 (ambos).
UMBRAL_ENLACE = [1]
UMBRAL_R1 = [0.5]
# Parámetros de R4
ALPHA = 0.3 # Balancea la popularidad y la distancia
# Ambos vectores deben ser de igual longitud
VECTOR_POPULARIDAD = [1,1,0,1,0,1,1,1]
VECTOR_DISTANCIA = [0,1,0,1,1,0,1,1]


# Divisor de la longitud de enlace dinámico.
# Se recomendan valores que sean potencia de 2, 
# p.e., 1, 2, 4, 8, 16, etc. 
LONG_ENLACES=[1,2,4]             
#--------EJECUCION---------------
# Semilla base para reproducir los experimentos. Si es None, cada corrida es
# aleatoria (como antes). Si es un entero, cada corrida recibe una semilla
# propia, distinta y reproducible, derivada de esta base, de su configuración
# y de su número de ejecución; se guarda en parametros.json y resumen.json dentro de la corrida.
SEMILLA_BASE = None
CICLOS=2                   # Número de ciclos de reconexión
EJECUCIONES = 2            # Número de ejecuciones por experimento   
#--------EXTRAS------------------
ENLACES_DINAMICOS=2        # Número de enlaces dinámicos por nodo
EXPLORADORES=4             # Número de paquetes exploradores por ciclo
# Divisor del máximo número de conexiones permitidas 
# máximo numero de conexiones permitidas=num_nodos/DIV_CONEXIONES
DIV_CONEXIONES=1            
#--------PARALELISMO--------------
# Número de procesos paralelos para ejecutar simulaciones
# Ajustar según el número de cores de la CPU
NUM_WORKERS=8