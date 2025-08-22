import config_paths as paths
import config
import config_Graficas as config_graficas

#PARA AGENTES COOPERADORES:
for i in config_graficas.REGLAS:
	for j in config_graficas.TOPOLOGIAS:
		for k in config_graficas.ALG_ENCAMINAMIENTO:
			LIST_CAPGEN=[]
			LIST_LTPGEN=[]
			LIST_DIAMGEN=[]
			LIST_GRAGEN=[]
			for l in config_graficas.TAM_ENLACES:
				primero=open(paths.RESULTADOS_DIR+"/"+l+"/ExperimentosCooperadores/"+i+"/"+j+"/"+k+"/datos-promedio.csv","r")
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
				grados=open(paths.RESULTADOS_DIR+"/"+l+"/ExperimentosCooperadores/"+i+"/"+j+"/"+k+"/datos-promedio_grados.csv","r")
				lineasgrados = grados.readlines()
				grados.close()
				LIST_GRAD=[]
				for contador,linea in enumerate(lineasgrados):
					if contador > 0:
						GRA=linea.replace("\n","").split(',')
						LIST_GRAD.append(GRA[1])
				LIST_GRAGEN.append(LIST_GRAD)
			#escribo el archivo csv final de cada experimento de base
			datosPromedio=open(paths.RESULTADOS_DIR+"/Gráficas_Formación/Cooperadores_"+i+"_"+j+"_"+k+".csv","w")
			datosPromedio.write(",Coeficiente de Agrupamiento\n,"+config_graficas.COLS_ENLACE+"\n")
			for contador,in1 in enumerate(range(len(LIST_CAPGEN[0]))):
				datosPromedio.write(str(contador)+",")
				for sublista in LIST_CAPGEN:
					datosPromedio.write(sublista[in1]+",")
				datosPromedio.write("\n")
			datosPromedio.write("\n\n,Longitud de Trayectoria Promedio\n,"+config_graficas.COLS_ENLACE+"\n")
			for contador,in1 in enumerate(range(len(LIST_LTPGEN[0]))):
				datosPromedio.write(str(contador)+",")
				for sublista in LIST_LTPGEN:
					datosPromedio.write(sublista[in1]+",")
				datosPromedio.write("\n")
			datosPromedio.write("\n\n,Diámetro\n,"+config_graficas.COLS_ENLACE+"\n")
			for contador,in1 in enumerate(range(len(LIST_DIAMGEN[0]))):
				datosPromedio.write(str(contador)+",")
				for sublista in LIST_DIAMGEN:
					datosPromedio.write(sublista[in1]+",")
				datosPromedio.write("\n")
			maximo=-99999
			for lista in LIST_GRAGEN:
				if len(lista)>maximo:
					maximo=len(lista)
			if config.RED=="anillo":
				nodos=config.NODOS_ANILLO
			else:
				nodos=config.ROWS*config.COLUMNS
			datosPromedio.write("\n\n,Distribución de Grados\n,"+config_graficas.COLS_ENLACE+"\n")
			for in1 in range(maximo):
				datosPromedio.write(str(in1)+",")
				for sublista in LIST_GRAGEN:
					try:
						datosPromedio.write(str(float(sublista[in1])/nodos)+",")
					except:
						datosPromedio.write(",")
				datosPromedio.write("\n")
			datosPromedio.close()

#PARA AGENTES SEMI-COOPERADORES:
for i in config_graficas.REGLAS_SC:
	for j in config_graficas.TOPOLOGIAS_SC:
		for k in config_graficas.CONEXIONES_SC:
			LIST_CAPGEN=[]
			LIST_LTPGEN=[]
			LIST_DIAMGEN=[]
			LIST_GRAGEN=[]
			for l in config_graficas.TAM_ENLACES_SC:
				try:
					primero=open(paths.RESULTADOS_DIR+"/"+l+"/ExperimentosSemi-Cooperadores/"+i+"/"+j+"/SP/"+k+"/datos-promedio.csv","r")
					lineasPrimero = primero.readlines()
					primero.close()
					LIST_CAP=[]
					LIST_LTP=[]
					LIST_DIAM=[]
					for contador,linea in enumerate(lineasPrimero):
						if contador > 0:
							CICLO,CAP,LTP,DIAM,a,b,c=linea.split(",")
							LIST_CAP.append(CAP)
							LIST_LTP.append(LTP)
							LIST_DIAM.append(DIAM.replace("\n",""))
					LIST_CAPGEN.append(LIST_CAP)
					LIST_LTPGEN.append(LIST_LTP)
					LIST_DIAMGEN.append(LIST_DIAM)
					grados=open(paths.RESULTADOS_DIR+"/"+l+"/ExperimentosSemi-Cooperadores/"+i+"/"+j+"/SP/"+k+"/datos-promedio_grados.csv","r")
					lineasgrados = grados.readlines()
					grados.close()
					LIST_GRAD=[]
					for contador,linea in enumerate(lineasgrados):
						if contador > 0:
							GRA=linea.replace("\n","").split(',')
							LIST_GRAD.append(GRA[1])
					LIST_GRAGEN.append(LIST_GRAD)
				except FileNotFoundError as error:
					pass
			#escribo el archivo csv final de cada experimento de semi-cooperadores
			datosPromedio=open(paths.RESULTADOS_DIR+"/Gráficas_Formación/Semi-Cooperadores_"+i+"_"+j+"_"+k+".csv","w")
			datosPromedio.write(",Coeficiente de Agrupamiento\n,"+config_graficas.COLS_ENLACE+"\n")
			for contador,in1 in enumerate(range(len(LIST_CAPGEN[0]))):
				datosPromedio.write(str(contador)+",")
				for sublista in LIST_CAPGEN:
					datosPromedio.write(sublista[in1]+",")
				datosPromedio.write("\n")
			datosPromedio.write("\n\n,Longitud de Trayectoria Promedio\n,"+config_graficas.COLS_ENLACE+"\n")
			for contador,in1 in enumerate(range(len(LIST_LTPGEN[0]))):
				datosPromedio.write(str(contador)+",")
				for sublista in LIST_LTPGEN:
					datosPromedio.write(sublista[in1]+",")
				datosPromedio.write("\n")
			datosPromedio.write("\n\n,Diámetro\n,"+config_graficas.COLS_ENLACE+"\n")
			for contador,in1 in enumerate(range(len(LIST_DIAMGEN[0]))):
				datosPromedio.write(str(contador)+",")
				for sublista in LIST_DIAMGEN:
					datosPromedio.write(sublista[in1]+",")
				datosPromedio.write("\n")
			maximo=-99999
			for lista in LIST_GRAGEN:
				if len(lista)>maximo:
					maximo=len(lista)
			if config.RED=="anillo":
				nodos=config.NODOS_ANILLO
			else:
				nodos=config.ROWS*config.COLUMNS
			datosPromedio.write("\n\n,Distribución de Grados\n,"+config_graficas.COLS_ENLACE+"\n")
			for in1 in range(maximo):
				datosPromedio.write(str(in1)+",")
				for sublista in LIST_GRAGEN:
					try:
						datosPromedio.write(str(float(sublista[in1])/nodos)+",")
					except:
						datosPromedio.write(",")
				datosPromedio.write("\n")
			datosPromedio.close()