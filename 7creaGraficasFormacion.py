import os
import configFormacion
import configPaths

os.makedirs(f"{configPaths.RESULTADOS_DIR}/Medidas_estructurales", exist_ok=True)


for r in configFormacion.REGLAS:
	for red in configFormacion.RED:
		if red == "anillo":
			nombre_red = "anillo" + str(configFormacion.NODOS_ANILLO)
		elif red == "malla":
			nombre_red = f"malla{configFormacion.ROWS}x{configFormacion.COLUMNS}"
		else:
			print(f" Tipo de red desconocido, saltando: {red}")
			continue 
		for ruteo in configFormacion.ROUTING:
			routing = "x"
			if ruteo == "COMPASS-ROUTING":
				routing = "CR"
			elif ruteo == "RANDOM-WALK":
				routing = "RW" 
			elif ruteo == "SHORTEST-PATH":
				routing = "SP"
			else:
				print(f" Algoritmo de ruteo desconocido, saltando: {ruteo}")
				continue
			LIST_CAPGEN=[]
			LIST_LTPGEN=[]
			LIST_DIAMGEN=[]
			LIST_GRAGEN=[]
			for long_enlace in configFormacion.LONG_ENLACES:
				#primero=open(experimentos.RESULTADOS_DIR+"/"+l+"/ExperimentosCooperadores/"+i+"/"+j+"/"+k+"/datos-promedio.csv","r")
				primero=open(f"{configPaths.RESULTADOS_DIR}/{nombre_red}/R{r}/{routing}/D{long_enlace}/datos-promedio.csv","r")
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
				grados=open(f"{configPaths.RESULTADOS_DIR}/{nombre_red}/R{r}/{routing}/D{long_enlace}/datos-promedio_grados.csv","r")
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
			datosPromedio=open(f"{configPaths.RESULTADOS_DIR}/Medidas_estructurales/Medidas_estructurales_{nombre_red}_R{r}_{routing}.csv","w")
			cols_enlace=""
			for long_enlace in configFormacion.LONG_ENLACES:
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
			if configFormacion.RED=="anillo":
				nodos=configFormacion.NODOS_ANILLO
			else:
				nodos=configFormacion.ROWS*configFormacion.COLUMNS
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