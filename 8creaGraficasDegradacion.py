import config_paths as paths
import config_Graficas as config_graficas

#PARA AGENTES COOPERADORES:
for p in config_graficas.DEGRADACION:
	for i in config_graficas.REGLAS:
		for j in config_graficas.TOPOLOGIAS:
			for k in config_graficas.ALG_ENCAMINAMIENTO:
				LIST_CAPGEN=[]
				LIST_LTPGEN=[]
				LIST_DIAMGEN=[]
				LIST_ORCGGEN=[]
				#LIST_ATTRGEN=[]
				LIST_ASSORTGEN=[]
				for l in config_graficas.TAM_ENLACES:
					primero=open(paths.DEGRADACION_DIR+"/"+p+"/GrafosFinales/"+l+"/ExperimentosCooperadores/"+i+"/"+j+"/"+k+"/datos-promedio.csv","r")
					lineasPrimero = primero.readlines()
					primero.close()
					LIST_CAP=[]
					LIST_LTP=[]
					LIST_DIAM=[]
					LIST_ORCG=[]
					#LIST_ATTR=[]
					LIST_ASSORT=[]
					for contador,linea in enumerate(lineasPrimero):
						if contador<(len(lineasPrimero)-4):#evito leer las ultimas 4 lineas de los archivos (muATTR, Modularidad y desviaciones estandar)
							#CAP,LTP,DIAM,ORCG,ATTR,ASSORT=linea.split(",")
							CAP,LTP,DIAM,ORCG,ASSORT=linea.split(",")
							LIST_CAP.append(CAP)
							LIST_LTP.append(LTP)
							LIST_DIAM.append(DIAM)
							LIST_ORCG.append(ORCG)
							#LIST_ATTR.append(ATTR)
							LIST_ASSORT.append(ASSORT.replace("\n",""))
					LIST_CAPGEN.append(LIST_CAP)
					LIST_LTPGEN.append(LIST_LTP)
					LIST_DIAMGEN.append(LIST_DIAM)
					LIST_ORCGGEN.append(LIST_ORCG)
					#LIST_ATTRGEN.append(LIST_ATTR)
					LIST_ASSORTGEN.append(LIST_ASSORT)
				#escribo el archivo csv final de cada experimento de base
				if p=="Fallas":
					datosPromedio=open(paths.DEGRADACION_DIR+"/Gráficas_Degradación_Fallas/FCooperadores_"+i+"_"+j+"_"+k+".csv","w")
				else:
					datosPromedio=open(paths.DEGRADACION_DIR+"/Gráficas_Degradación_Ataques/ACooperadores_"+i+"_"+j+"_"+k+".csv","w")
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
				datosPromedio.write("\n\n,Orden Relativo del Componente Gigante\n,"+config_graficas.COLS_ENLACE+"\n")
				for contador,in1 in enumerate(range(len(LIST_ORCGGEN[0]))):
					datosPromedio.write(str(contador)+",")
					for sublista in LIST_ORCGGEN:
						datosPromedio.write(sublista[in1]+",")
					datosPromedio.write("\n")
				#datosPromedio.write("\n\n,ATTR\n,"+config_graficas.COLS_ENLACE+"\n")
				#for contador,in1 in enumerate(range(len(LIST_ATTRGEN[0]))):
				#	datosPromedio.write(str(contador)+",")
				#	for sublista in LIST_ATTRGEN:
				#		datosPromedio.write(sublista[in1]+",")
				#	datosPromedio.write("\n")
				datosPromedio.write("\n\n,ASSORT\n,"+config_graficas.COLS_ENLACE+"\n")
				for contador,in1 in enumerate(range(len(LIST_ASSORTGEN[0]))):
					datosPromedio.write(str(contador)+",")
					for sublista in LIST_ASSORTGEN:
						datosPromedio.write(sublista[in1]+",")
					datosPromedio.write("\n")
				datosPromedio.close()

#PARA AGENTES SEMI-COOPERADORES:
for p in config_graficas.DEGRADACION:
	for i in config_graficas.REGLAS_SC:
		for j in config_graficas.TOPOLOGIAS_SC:
			for k in config_graficas.CONEXIONES_SC:
				LIST_CAPGEN=[]
				LIST_LTPGEN=[]
				LIST_DIAMGEN=[]
				LIST_ORCGGEN=[]
				#LIST_ATTRGEN=[]
				LIST_ASSORTGEN=[]
				for l in config_graficas.TAM_ENLACES_SC:
					try:
						primero=open(paths.DEGRADACION_DIR+p+"/GrafosFinales/"+l+"/ExperimentosSemi-Cooperadores/"+i+"/"+j+"/SP/"+k+"/datos-promedio.csv","r")
						lineasPrimero = primero.readlines()
						primero.close()
						LIST_CAP=[]
						LIST_LTP=[]
						LIST_DIAM=[]
						LIST_ORCG=[]
						#LIST_ATTR=[]
						LIST_ASSORT=[]
						for contador,linea in enumerate(lineasPrimero):
							if contador<(len(lineasPrimero)-4):#evito leer las ultimas 4 lineas de los archivos (muATTR, Modularidad y desviaciones estandar)
								#CAP,LTP,DIAM,ORCG,ATTR,ASSORT=linea.split(",")
								CAP,LTP,DIAM,ORCG,ASSORT=linea.split(",")
								LIST_CAP.append(CAP)
								LIST_LTP.append(LTP)
								LIST_DIAM.append(DIAM)
								LIST_ORCG.append(ORCG)
								#LIST_ATTR.append(ATTR)
								LIST_ASSORT.append(ASSORT.replace("\n",""))
						LIST_CAPGEN.append(LIST_CAP)
						LIST_LTPGEN.append(LIST_LTP)
						LIST_DIAMGEN.append(LIST_DIAM)
						LIST_ORCGGEN.append(LIST_ORCG)
						#LIST_ATTRGEN.append(LIST_ATTR)
						LIST_ASSORTGEN.append(LIST_ASSORT)
					except FileNotFoundError as error:
						pass
				#escribo el archivo csv final de cada experimento de semi-cooperadores
				if p=="Fallas":
					datosPromedio=open(paths.DEGRADACION_DIR+"Gráficas_Degradación_Fallas/FSemi-Cooperadores_"+i+"_"+j+"_"+k+".csv","w")
				else:
					datosPromedio=open(paths.DEGRADACION_DIR+"Gráficas_Degradación_Ataques/ASemi-Cooperadores_"+i+"_"+j+"_"+k+".csv","w")
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
				datosPromedio.write("\n\n,Orden Relativo del Componente Gigante\n,"+config_graficas.COLS_ENLACE+"\n")
				for contador,in1 in enumerate(range(len(LIST_ORCGGEN[0]))):
					datosPromedio.write(str(contador)+",")
					for sublista in LIST_ORCGGEN:
						datosPromedio.write(sublista[in1]+",")
					datosPromedio.write("\n")
				#datosPromedio.write("\n\n,ATTR\n,"+config_graficas.COLS_ENLACE+"\n")
				#for contador,in1 in enumerate(range(len(LIST_ATTRGEN[0]))):
				#	datosPromedio.write(str(contador)+",")
				#	for sublista in LIST_ATTRGEN:
				#		datosPromedio.write(sublista[in1]+",")
				#	datosPromedio.write("\n")
				datosPromedio.write("\n\n,ASSORT\n,"+config_graficas.COLS_ENLACE+"\n")
				for contador,in1 in enumerate(range(len(LIST_ASSORTGEN[0]))):
					datosPromedio.write(str(contador)+",")
					for sublista in LIST_ASSORTGEN:
						datosPromedio.write(sublista[in1]+",")
					datosPromedio.write("\n")
				datosPromedio.close()