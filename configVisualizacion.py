import configuracion
import redes
from formacion import ABREVIATURAS
#Configuración para la visualización de los resultados de experimentos.s
#--------VISUALIZACION-----------
#Parametros para 3creaImagenesPNG.py
# Se recomiendan los siguientes valores:
# 1 para orden de anillo=1500 y orden de malla=2500
# 20 para orden de anillo=50 y orden de malla=64
NODE_SCALE = 20    

#Parametros para 9creaGraficasResumenFinal.py         
COLS_ENLACE = "" #"D,D2,D4"
TAM_ENLACES = []
for i in range(len(configuracion.LONG_ENLACES)):
    l = configuracion.LONG_ENLACES[i]
    if l == 1:
        COLS_ENLACE+="D"
        TAM_ENLACES.append("D")
    else:
        COLS_ENLACE+=",D"+str(l)
        TAM_ENLACES.append("D"+str(l))
    if i < len(configuracion.LONG_ENLACES)-1:
        COLS_ENLACE+=","
    
COLS_REGLAS = ""
REGLAS = []
for i in range(len(configuracion.REGLAS)):
    l = configuracion.REGLAS[i]
    COLS_REGLAS+=",R"+str(l)
    REGLAS.append("R"+str(l))
    if i < len(configuracion.REGLAS)-1:
        COLS_REGLAS+=","

# Abreviaturas de las exploraciones, las mismas que usa formacion.py en los nombres de carpeta
COLS_ROUTING = [ABREVIATURAS[r] for r in configuracion.ROUTING if r in ABREVIATURAS]

COLS_CONEXIONES = "n"
#PARA AGENTES COOPERADORES:
# Nombres de las carpetas de cada red, p.e. ["malla8x8","anillo64"]
TOPOLOGIAS = [redes.obtener_red(r, configuracion).nombre() for r in configuracion.RED if r in redes.REDES]
ALG_ENCAMINAMIENTO=COLS_ROUTING

#PARA AGENTES SEMI-COOPERADORES:
#TAM_ENLACES_SC=["D","D2","D4"]
#REGLAS_SC=[]#["R1","R2","R3"]
#TOPOLOGIAS_SC=["malla8x8","anillo50"]
#CONEXIONES_SC=["n4","n16","n64"]

#PARA AGENTES DEGRADACION:
#DEGRADACION=configDegradacion.TIPO_DEGRADACION  #["Fallas","Ataques"]