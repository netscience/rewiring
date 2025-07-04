#Configuración del experimento
#--------ANILLO------------------
NODOS_ANILLO=1500           # Número de nodos del anillo
#--------MALLA-------------------
ROWS=8                      # Filas de la malla
COLUMNS=8                   # Columnas de la malla
#--------EXPERIMENTO-------------
ROUTING="COMPASS-ROUTING"   # Algoritmo de encaminamiento: "COMPASS-ROUTING", "RANDOM-WALK", "SHORTEST-PATH"
REGLA=1                     # 1,2,3
LONG_ENLACE=1               # Divisor de la longitud de enlace dinámico: 1, 2, 4, 8, 16, 32 
#--------EJECUCION---------------
CICLOS=5                    # Número de ciclos de simulación
#--------EXTRAS------------------
ENLACES_DINAMICOS=2         # Número de enlaces dinámicos por nodo
EXPLORADORES=20             # Número de paquetes exploradores por ciclo
DIV_CONEXIONES=1          # Divisor (con respecto al número de nodos, num_nodos/DIV_CONEXIONES) del máximo número de conexiones permitidas
#--------VISUALIZACION-----------
#Parameteros para 3creaImagenesPNG.py
NODE_SCALE = 10 #Usar 1 para orden de anillo=1500 y orde de malla=2500