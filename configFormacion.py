#Configuración de una serie de experimentos de formación de redes
#--------ANILLO------------------
NODOS_ANILLO=50             # Número de nodos del anillo. Colocar 0 si no se usa anillo
#--------MALLA-------------------
ROWS=20                      # Filas de la malla. Colocar 0 si no se usa malla
COLUMNS=20                   # Columnas de la malla
#--------FORMACION-------------
# Estos parámetros se deben definir como lista aunque contengan un solo valor
RED=["malla"]#,"anillo"]  # Tipo de red: "malla", "anillo"
ROUTING=["SHORTEST-PATH"]#,"COMPASS-ROUTING","RANDOM-WALK"]                # Algoritmo de encaminamiento: "COMPASS-ROUTING", "RANDOM-WALK", "SHORTEST-PATH"
REGLAS=[4]              # 1,2,3
LONG_ENLACES=[1]         # Divisor de la longitud de enlace dinámico: 1, 2, 4, 8, 16, 32 
#--------REGLA 4--------------
ALPHA=1          # Valor de alfa para la regla 4: 0.0, 0.5, 1.
# Ambos vectores deben tener la misma longitud
VECTOR_POPULARIDAD = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]  # Vector de popularidad para la regla 4
VECTOR_DISTANCIA   = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]      # Vector de distancia para la regla 4
#--------EJECUCION---------------
CICLOS=5                    # Número de ciclos de recableo
EJECUCIONES = 4            # Número de ejecuciones por experimento   
#--------EXTRAS------------------
ENLACES_DINAMICOS=2         # Número de enlaces dinámicos por nodo
EXPLORADORES=6             # Número de paquetes exploradores por ciclo
# Divisor del máximo número de conexiones permitidas (máximo numero de conexiones permitidas=num_nodos/DIV_CONEXIONES)
DIV_CONEXIONES=1            