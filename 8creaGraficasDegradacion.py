import os
import configPaths
import configDegradacion
import configFormacion

for tipo_degradacion in configDegradacion.TIPO_DEGRADACION:
	os.makedirs(f"{configPaths.DEGRADACION_DIR}/Medidas_degradacion/Medidas_{tipo_degradacion}", exist_ok=True)
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
				LIST_ORCGGEN=[]
				#LIST_ATTRGEN=[]
				LIST_ASSORTGEN=[]
				for long_enlace in configFormacion.LONG_ENLACES:
					dir_degradacion=configPaths.DEGRADACION_DIR+"/"+tipo_degradacion+"/"+nombre_red+"/R"+str(r)+"/"+routing+"/D"+str(long_enlace)+"/"
					primero=open(dir_degradacion+"datos-promedio.csv","r")
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
				cols_enlace=""
				for long_enlace in configFormacion.LONG_ENLACES:
					cols_enlace=cols_enlace+"D"+str(long_enlace)+","
			
				datosPromedio=open(configPaths.DEGRADACION_DIR+"/Medidas_degradacion/Medidas_"+tipo_degradacion+"/Medidas_"+tipo_degradacion+"_"+nombre_red+"_R"+str(r)+"_"+routing+".csv","w")
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
				datosPromedio.write("\n\n,Orden Relativo del Componente Gigante\n,"+cols_enlace+"\n")
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
				datosPromedio.write("\n\n,ASSORT\n,"+cols_enlace+"\n")
				for contador,in1 in enumerate(range(len(LIST_ASSORTGEN[0]))):
					datosPromedio.write(str(contador)+",")
					for sublista in LIST_ASSORTGEN:
						datosPromedio.write(sublista[in1]+",")
					datosPromedio.write("\n")
				datosPromedio.close()