import os
import configuracion
import formacion
import redes

os.makedirs(f"{configuracion.RESULTADOS_DIR}/Medidas_estructurales", exist_ok=True)

# Una tabla por cada (red, regla, exploración), con una columna por longitud de enlace.
# Las configuraciones y los nombres de carpeta son los mismos que usa formacion.py,
# de modo que se incluyen todas las exploraciones (RWD, RWI y cada pareja (p, q) de Node2Vec).
grupos = {}
for ruta, par in formacion.plan():
	base = ruta.rsplit("/D", 1)[0]
	grupos.setdefault(base, par)

for base, par in grupos.items():
	nombre_red, regla, routing = base.split("/")[-3:]
	r = regla[1:]
	# Número de nodos de la red, para normalizar la distribución de grados
	nodos = redes.obtener_red(par.red, par.cfg_red()).construir().number_of_nodes()
	LIST_CAPGEN=[]
	LIST_LTPGEN=[]
	LIST_DIAMGEN=[]
	LIST_GRAGEN=[]
	faltantes = [l for l in configuracion.LONG_ENLACES
	             if not os.path.exists(f"{base}/D{l}/datos-promedio.csv")]
	if faltantes:
		print(f" Falta datos-promedio.csv en {base} (D{faltantes}); corre antes 1creaPromediosFormacion.py y 2creaPromediosDistGradosFormacion.py. Saltando.")
		continue
	for long_enlace in configuracion.LONG_ENLACES:
		primero=open(f"{base}/D{long_enlace}/datos-promedio.csv","r")
		lineasPrimero = primero.readlines()
		primero.close()
		LIST_CICLO=[]
		LIST_CAP=[]
		LIST_LTP=[]
		LIST_DIAM=[]
		for contador,linea in enumerate(lineasPrimero):
			if contador > 0:
				CICLO,CAP,LTP,DIAM,a,b,c=linea.split(",")
				LIST_CICLO.append(CICLO)
				LIST_CAP.append(CAP)
				LIST_LTP.append(LTP)
				LIST_DIAM.append(DIAM.replace("\n",""))
		LIST_CAPGEN.append(LIST_CAP)
		LIST_LTPGEN.append(LIST_LTP)
		LIST_DIAMGEN.append(LIST_DIAM)
		grados=open(f"{base}/D{long_enlace}/datos-promedio_grados.csv","r")
		lineasgrados = grados.readlines()
		grados.close()
		LIST_GRAD=[]
		for contador,linea in enumerate(lineasgrados):
			if contador > 0:
				GRA=linea.replace("\n","").split(',')
				LIST_GRAD.append(GRA[1])
		LIST_GRAGEN.append(LIST_GRAD)
	#escribo el archivo csv final de cada experimento de base
	#datosPromedio=open(experimentos.RESULTADOS_DIR+"/Gráficas_Formación/Cooperadores_"+i+"_"+j+"_"+k+".csv","w")
	datosPromedio=open(f"{configuracion.RESULTADOS_DIR}/Medidas_estructurales/Medidas_estructurales_{nombre_red}_R{r}_{routing}.csv","w")
	cols_enlace=""
	for long_enlace in configuracion.LONG_ENLACES:
		cols_enlace=cols_enlace+"D"+str(long_enlace)+","
	datosPromedio.write(",Coeficiente de Agrupamiento\n,"+cols_enlace+"\n")
	for contador,in1 in enumerate(range(len(LIST_CAPGEN[0]))):
		datosPromedio.write(str(contador)+",")
		for sublista in LIST_CAPGEN:
			datosPromedio.write(sublista[in1]+",")
		datosPromedio.write("\n")
	datosPromedio.write("\n\n,Longitud de Trayectoria Promedio\n,"+cols_enlace+"\n")
	for contador,in1 in enumerate(range(len(LIST_LTPGEN[0]))):
		datosPromedio.write(str(contador)+",")
		for sublista in LIST_LTPGEN:
			datosPromedio.write(sublista[in1]+",")
		datosPromedio.write("\n")
	datosPromedio.write("\n\n,Diámetro\n,"+cols_enlace+"\n")
	for contador,in1 in enumerate(range(len(LIST_DIAMGEN[0]))):
		datosPromedio.write(str(contador)+",")
		for sublista in LIST_DIAMGEN:
			datosPromedio.write(sublista[in1]+",")
		datosPromedio.write("\n")
	maximo=-99999
	for lista in LIST_GRAGEN:
		if len(lista)>maximo:
			maximo=len(lista)
	datosPromedio.write("\n\n,Distribución de Grados\n,"+cols_enlace+"\n")
	for in1 in range(maximo):
		datosPromedio.write(str(in1)+",")
		for sublista in LIST_GRAGEN:
			try:
				datosPromedio.write(str(float(sublista[in1])/nodos)+",")
			except:
				datosPromedio.write(",")
		datosPromedio.write("\n")
	datosPromedio.close()