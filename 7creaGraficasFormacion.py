
directorio="C:\\Users\\VG\\Documents\\Formación\\"

#PARA AGENTES COOPERADORES:
tamEnlaces=["D","D2","D4","D8","D16"]
reglas=["R1","R2","R3"]
topologias=["anillo1500","malla50x50"]
algEncaminamiento=["CR","RW","SP"]
for i in reglas:
	for j in topologias:
		for k in algEncaminamiento:
			LIST_CAPGEN=[]
			LIST_LTPGEN=[]
			LIST_DIAMGEN=[]
			LIST_GRAGEN=[]
			for l in tamEnlaces:
				primero=open(directorio+l+"\\ExperimentosCooperadores\\"+i+"\\"+j+"\\"+k+"\\datos-promedio.csv","r")
				lineasPrimero = primero.readlines()
				primero.close()
				LIST_CAP=[]
				LIST_LTP=[]
				LIST_DIAM=[]
				for contador,linea in enumerate(lineasPrimero):
					CAP,LTP,DIAM,a,b,c=linea.split(",")
					LIST_CAP.append(CAP)
					LIST_LTP.append(LTP)
					LIST_DIAM.append(DIAM.replace("\n",""))
				LIST_CAPGEN.append(LIST_CAP)
				LIST_LTPGEN.append(LIST_LTP)
				LIST_DIAMGEN.append(LIST_DIAM)
				grados=open(directorio+l+"\\ExperimentosCooperadores\\"+i+"\\"+j+"\\"+k+"\\datos-promedio_grados.csv","r")
				lineasgrados = grados.readlines()
				grados.close()
				LIST_GRAD=[]
				for contador,linea in enumerate(lineasgrados):
					GRA=linea.replace("\n","")
					LIST_GRAD.append(GRA)
				LIST_GRAGEN.append(LIST_GRAD)
			#escribo el archivo csv final de cada experimento de base
			datosPromedio=open(directorio+"Gráficas_Formación\\Cooperadores_"+i+"_"+j+"_"+k+".csv","w")
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
			maximo=-99999
			for lista in LIST_GRAGEN:
				if len(lista)>maximo:
					maximo=len(lista)
			if j=="anillo1500":
				nodos=1500
			else:
				nodos=2500
			datosPromedio.write("\n\n,Distribución de Grados\n,D,D2,D4,D8,D16\n")
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
tamEnlaces=["D","D2","D4","D8","D16"]
reglas=["R1","R2","R3"]
topologias=["anillo1500","malla50x50"]
conexionesMaximas=["n4","n16","n64"]
for i in reglas:
	for j in topologias:
		for k in conexionesMaximas:
			LIST_CAPGEN=[]
			LIST_LTPGEN=[]
			LIST_DIAMGEN=[]
			LIST_GRAGEN=[]
			for l in tamEnlaces:
				try:
					primero=open(directorio+l+"\\ExperimentosSemi-Cooperadores\\"+i+"\\"+j+"\\SP\\"+k+"\\datos-promedio.csv","r")
					lineasPrimero = primero.readlines()
					primero.close()
					LIST_CAP=[]
					LIST_LTP=[]
					LIST_DIAM=[]
					for contador,linea in enumerate(lineasPrimero):
						CAP,LTP,DIAM,a,b,c=linea.split(",")
						LIST_CAP.append(CAP)
						LIST_LTP.append(LTP)
						LIST_DIAM.append(DIAM.replace("\n",""))
					LIST_CAPGEN.append(LIST_CAP)
					LIST_LTPGEN.append(LIST_LTP)
					LIST_DIAMGEN.append(LIST_DIAM)
					grados=open(directorio+l+"\\ExperimentosSemi-Cooperadores\\"+i+"\\"+j+"\\SP\\"+k+"\\datos-promedio_grados.csv","r")
					lineasgrados = grados.readlines()
					grados.close()
					LIST_GRAD=[]
					for contador,linea in enumerate(lineasgrados):
						GRA=linea.replace("\n","")
						LIST_GRAD.append(GRA)
					LIST_GRAGEN.append(LIST_GRAD)
				except FileNotFoundError as error:
					pass
			#escribo el archivo csv final de cada experimento de semi-cooperadores
			datosPromedio=open(directorio+"Gráficas_Formación\\Semi-Cooperadores_"+i+"_"+j+"_"+k+".csv","w")
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
			maximo=-99999
			for lista in LIST_GRAGEN:
				if len(lista)>maximo:
					maximo=len(lista)
			if j=="anillo1500":
				nodos=1500
			else:
				nodos=2500
			datosPromedio.write("\n\n,Distribución de Grados\n,D,D2,D4,D8,D16\n")
			for in1 in range(maximo):
				datosPromedio.write(str(in1)+",")
				for sublista in LIST_GRAGEN:
					try:
						datosPromedio.write(str(float(sublista[in1])/nodos)+",")
					except:
						datosPromedio.write(",")
				datosPromedio.write("\n")
			datosPromedio.close()