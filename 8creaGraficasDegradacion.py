
directorio="C:\\Users\\VG\\Documents\\Degradación\\"

#PARA AGENTES COOPERADORES:
tiposDegradacion=["Fallas","Ataques"]
tamEnlaces=["D","D2","D4","D8","D16"]
reglas=["R1","R2","R3"]
topologias=["anillo1500","malla50x50"]
algEncaminamiento=["CR","RW","SP"]
for p in tiposDegradacion:
	for i in reglas:
		for j in topologias:
			for k in algEncaminamiento:
				LIST_CAPGEN=[]
				LIST_LTPGEN=[]
				LIST_DIAMGEN=[]
				LIST_ORCGGEN=[]
				LIST_ATTRGEN=[]
				LIST_ASSORTGEN=[]
				for l in tamEnlaces:
					primero=open(directorio+p+"\\GrafosFinales\\"+l+"\\ExperimentosCooperadores\\"+i+"\\"+j+"\\"+k+"\\datos-promedio.csv","r")
					lineasPrimero = primero.readlines()
					primero.close()
					LIST_CAP=[]
					LIST_LTP=[]
					LIST_DIAM=[]
					LIST_ORCG=[]
					LIST_ATTR=[]
					LIST_ASSORT=[]
					for contador,linea in enumerate(lineasPrimero):
						if contador<(len(lineasPrimero)-4):#evito leer las ultimas 4 lineas de los archivos (muATTR, Modularidad y desviaciones estandar)
							CAP,LTP,DIAM,ORCG,ATTR,ASSORT=linea.split(",")
							LIST_CAP.append(CAP)
							LIST_LTP.append(LTP)
							LIST_DIAM.append(DIAM)
							LIST_ORCG.append(ORCG)
							LIST_ATTR.append(ATTR)
							LIST_ASSORT.append(ASSORT.replace("\n",""))
					LIST_CAPGEN.append(LIST_CAP)
					LIST_LTPGEN.append(LIST_LTP)
					LIST_DIAMGEN.append(LIST_DIAM)
					LIST_ORCGGEN.append(LIST_ORCG)
					LIST_ATTRGEN.append(LIST_ATTR)
					LIST_ASSORTGEN.append(LIST_ASSORT)
				#escribo el archivo csv final de cada experimento de base
				if p=="Fallas":
					datosPromedio=open(directorio+"Gráficas_Degradación_Fallas\\FCooperadores_"+i+"_"+j+"_"+k+".csv","w")
				else:
					datosPromedio=open(directorio+"Gráficas_Degradación_Ataques\\ACooperadores_"+i+"_"+j+"_"+k+".csv","w")
				datosPromedio.write(",Coeficiente de Agrupamiento\n,D,D2,D4,D8,D16\n")
				for contador,in1 in enumerate(range(len(LIST_CAPGEN[0]))):
					datosPromedio.write(str(contador)+",")
					for sublista in LIST_CAPGEN:
						datosPromedio.write(sublista[in1]+",")
					datosPromedio.write("\n")
				datosPromedio.write("\n\n,Longitud de Trayectoria Promedio\n,D,D2,D4,D8,D16\n")
				for contador,in1 in enumerate(range(len(LIST_LTPGEN[0]))):
					datosPromedio.write(str(contador)+",")
					for sublista in LIST_LTPGEN:
						datosPromedio.write(sublista[in1]+",")
					datosPromedio.write("\n")
				datosPromedio.write("\n\n,Diámetro\n,D,D2,D4,D8,D16\n")
				for contador,in1 in enumerate(range(len(LIST_DIAMGEN[0]))):
					datosPromedio.write(str(contador)+",")
					for sublista in LIST_DIAMGEN:
						datosPromedio.write(sublista[in1]+",")
					datosPromedio.write("\n")
				datosPromedio.write("\n\n,Orden Relativo del Componente Gigante\n,D,D2,D4,D8,D16\n")
				for contador,in1 in enumerate(range(len(LIST_ORCGGEN[0]))):
					datosPromedio.write(str(contador)+",")
					for sublista in LIST_ORCGGEN:
						datosPromedio.write(sublista[in1]+",")
					datosPromedio.write("\n")
				datosPromedio.write("\n\n,ATTR\n,D,D2,D4,D8,D16\n")
				for contador,in1 in enumerate(range(len(LIST_ATTRGEN[0]))):
					datosPromedio.write(str(contador)+",")
					for sublista in LIST_ATTRGEN:
						datosPromedio.write(sublista[in1]+",")
					datosPromedio.write("\n")
				datosPromedio.write("\n\n,ASSORT\n,D,D2,D4,D8,D16\n")
				for contador,in1 in enumerate(range(len(LIST_ASSORTGEN[0]))):
					datosPromedio.write(str(contador)+",")
					for sublista in LIST_ASSORTGEN:
						datosPromedio.write(sublista[in1]+",")
					datosPromedio.write("\n")
				datosPromedio.close()

#PARA AGENTES SEMI-COOPERADORES:
tiposDegradacion=["Fallas","Ataques"]
tamEnlaces=["D","D2","D4","D8","D16"]
reglas=["R1","R2","R3"]
topologias=["anillo1500","malla50x50"]
conexionesMaximas=["n4","n16","n64"]
for p in tiposDegradacion:
	for i in reglas:
		for j in topologias:
			for k in conexionesMaximas:
				LIST_CAPGEN=[]
				LIST_LTPGEN=[]
				LIST_DIAMGEN=[]
				LIST_ORCGGEN=[]
				LIST_ATTRGEN=[]
				LIST_ASSORTGEN=[]
				for l in tamEnlaces:
					try:
						primero=open(directorio+p+"\\GrafosFinales\\"+l+"\\ExperimentosSemi-Cooperadores\\"+i+"\\"+j+"\\SP\\"+k+"\\datos-promedio.csv","r")
						lineasPrimero = primero.readlines()
						primero.close()
						LIST_CAP=[]
						LIST_LTP=[]
						LIST_DIAM=[]
						LIST_ORCG=[]
						LIST_ATTR=[]
						LIST_ASSORT=[]
						for contador,linea in enumerate(lineasPrimero):
							if contador<(len(lineasPrimero)-4):#evito leer las ultimas 4 lineas de los archivos (muATTR, Modularidad y desviaciones estandar)
								CAP,LTP,DIAM,ORCG,ATTR,ASSORT=linea.split(",")
								LIST_CAP.append(CAP)
								LIST_LTP.append(LTP)
								LIST_DIAM.append(DIAM)
								LIST_ORCG.append(ORCG)
								LIST_ATTR.append(ATTR)
								LIST_ASSORT.append(ASSORT.replace("\n",""))
						LIST_CAPGEN.append(LIST_CAP)
						LIST_LTPGEN.append(LIST_LTP)
						LIST_DIAMGEN.append(LIST_DIAM)
						LIST_ORCGGEN.append(LIST_ORCG)
						LIST_ATTRGEN.append(LIST_ATTR)
						LIST_ASSORTGEN.append(LIST_ASSORT)
					except FileNotFoundError as error:
						pass
				#escribo el archivo csv final de cada experimento de semi-cooperadores
				if p=="Fallas":
					datosPromedio=open(directorio+"Gráficas_Degradación_Fallas\\FSemi-Cooperadores_"+i+"_"+j+"_"+k+".csv","w")
				else:
					datosPromedio=open(directorio+"Gráficas_Degradación_Ataques\\ASemi-Cooperadores_"+i+"_"+j+"_"+k+".csv","w")
				datosPromedio.write(",Coeficiente de Agrupamiento\n,D,D2,D4,D8,D16\n")
				for contador,in1 in enumerate(range(len(LIST_CAPGEN[0]))):
					datosPromedio.write(str(contador)+",")
					for sublista in LIST_CAPGEN:
						datosPromedio.write(sublista[in1]+",")
					datosPromedio.write("\n")
				datosPromedio.write("\n\n,Longitud de Trayectoria Promedio\n,D,D2,D4,D8,D16\n")
				for contador,in1 in enumerate(range(len(LIST_LTPGEN[0]))):
					datosPromedio.write(str(contador)+",")
					for sublista in LIST_LTPGEN:
						datosPromedio.write(sublista[in1]+",")
					datosPromedio.write("\n")
				datosPromedio.write("\n\n,Diámetro\n,D,D2,D4,D8,D16\n")
				for contador,in1 in enumerate(range(len(LIST_DIAMGEN[0]))):
					datosPromedio.write(str(contador)+",")
					for sublista in LIST_DIAMGEN:
						datosPromedio.write(sublista[in1]+",")
					datosPromedio.write("\n")
				datosPromedio.write("\n\n,Orden Relativo del Componente Gigante\n,D,D2,D4,D8,D16\n")
				for contador,in1 in enumerate(range(len(LIST_ORCGGEN[0]))):
					datosPromedio.write(str(contador)+",")
					for sublista in LIST_ORCGGEN:
						datosPromedio.write(sublista[in1]+",")
					datosPromedio.write("\n")
				datosPromedio.write("\n\n,ATTR\n,D,D2,D4,D8,D16\n")
				for contador,in1 in enumerate(range(len(LIST_ATTRGEN[0]))):
					datosPromedio.write(str(contador)+",")
					for sublista in LIST_ATTRGEN:
						datosPromedio.write(sublista[in1]+",")
					datosPromedio.write("\n")
				datosPromedio.write("\n\n,ASSORT\n,D,D2,D4,D8,D16\n")
				for contador,in1 in enumerate(range(len(LIST_ASSORTGEN[0]))):
					datosPromedio.write(str(contador)+",")
					for sublista in LIST_ASSORTGEN:
						datosPromedio.write(sublista[in1]+",")
					datosPromedio.write("\n")
				datosPromedio.close()