import configFormacion
#Configuración para la visualización de los resultados de experimentos.s
#--------VISUALIZACION-----------
#Parametros para 3creaImagenesPNG.py
# Se recomiendan los siguientes valores:
# 1 para orden de anillo=1500 y orden de malla=2500
# 20 para orden de anillo=50 y orden de malla=64
NODE_SCALE = 20    

#Parametros para 9creaGraficasResumenFinal.py         
COLS_ENLACE = "" #"D,D2,D4"
for i in range(len(configFormacion.LONG_ENLACES)):
    l = configFormacion.LONG_ENLACES[i]
    if l == 1:
        COLS_ENLACE+="D"
    else:
        COLS_ENLACE+=",D"+str(l)
    if i < len(configFormacion.LONG_ENLACES)-1:
        COLS_ENLACE+=","
    
COLS_REGLAS = ""
for i in range(len(configFormacion.REGLAS)):
    l = configFormacion.REGLAS[i]
    COLS_REGLAS+=",R"+str(l)
    if i < len(configFormacion.REGLAS)-1:
        COLS_REGLAS+=","

COLS_ROUTING = "SP,CR,RW"
COLS_CONEXIONES = "n"
#PARA AGENTES COOPERADORES:
TAM_ENLACES=["D","D2","D4"]
REGLAS=["R1","R2","R3"]
TOPOLOGIAS=["malla8x8","anillo50"]
ALG_ENCAMINAMIENTO=["SP","CR","RW"]

#PARA AGENTES SEMI-COOPERADORES:
TAM_ENLACES_SC=["D","D2","D4"]
REGLAS_SC=[]#["R1","R2","R3"]
TOPOLOGIAS_SC=["malla8x8","anillo50"]
CONEXIONES_SC=["n4","n16","n64"]

#PARA AGENTES DEGRADACION:
DEGRADACION=["Fallas","Ataques"]