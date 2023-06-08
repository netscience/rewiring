#crea un resumen de las medidas promedio obtenidas previamente de la parte de formacion y degradacion de redes complejas

#tamaños de enlaces vs reglas de recableado
#experimentos cooperadores:
ejemplo_dir = 'C:\\Users\\VG\\Documents\\Formación'
ejemplo_dir2 = 'C:\\Users\\VG\\Documents\\Degradación\\Ataques\\GrafosFinales'
ejemplo_dir3 = 'C:\\Users\\VG\\Documents\\Degradación\\Fallas\\GrafosFinales'
tamEnlace=["D","D2","D4","D8","D16"]
reglas=["R1","R2","R3"]
topologias=["anillo1500","malla50x50"]
algEncam=["CR","RW","SP"]
medidas=["CAP","LTP","DIAM","GRADO_MAX","ATTR"]
for p in topologias:
	for i in algEncam:
		archivo=open("Coop-"+p+"-"+i+".csv","w")
		for contador,j in enumerate(medidas):
			archivo.write("\n"+j+",R1,R2,R3\n")
			if contador<3:
				for k in tamEnlace:
					escribir=[k]
					for l in reglas:
						arch=open(ejemplo_dir+"\\"+k+"\\ExperimentosCooperadores\\"+l+"\\"+p+"\\"+i+"\\datos-promedio.csv","r")
						lineas=arch.readlines()
						arch.close()
						CAP,LTP,DIAM,a,b,c=lineas[len(lineas)-1].replace("\n","").split(",")
						lineaLista=[CAP,LTP,DIAM]
						escribir.append(lineaLista[contador])
					archivo.write(escribir[0]+","+escribir[1]+","+escribir[2]+","+escribir[3]+"\n")
			else:
				if contador==3:
					for k in tamEnlace:
						escribir=[k]
						for l in reglas:
							arch=open(ejemplo_dir+"\\"+k+"\\ExperimentosCooperadores\\"+l+"\\"+p+"\\"+i+"\\datos-promedio_grados.csv","r")
							lineas=arch.readlines()
							arch.close()
							escribir.append(str(len(lineas)-1))
						archivo.write(escribir[0]+","+escribir[1]+","+escribir[2]+","+escribir[3]+"\n")
				else:
					for k in tamEnlace:
						escribir=[k]
						for l in reglas:
							arch=open(ejemplo_dir2+"\\"+k+"\\ExperimentosCooperadores\\"+l+"\\"+p+"\\"+i+"\\datos-promedio.csv","r")
							lineas=arch.readlines()
							arch.close()
							CAP,LTP,DIAM,ORCG,ATTR,ASSORT=lineas[29].replace("\n","").split(",")
							lineaLista=[CAP,LTP,DIAM,ORCG,ATTR]
							escribir.append(lineaLista[contador])
						archivo.write(escribir[0]+","+escribir[1]+","+escribir[2]+","+escribir[3]+"\n")
					archivo.write("\n"+"LTP"+",R1,R2,R3\n")
					for k in tamEnlace:
						escribir=[k]
						for l in reglas:
							arch=open(ejemplo_dir2+"\\"+k+"\\ExperimentosCooperadores\\"+l+"\\"+p+"\\"+i+"\\datos-promedio.csv","r")
							lineas=arch.readlines()
							arch.close()
							CAP,LTP,DIAM,ORCG,ATTR,ASSORT=lineas[29].replace("\n","").split(",")
							escribir.append(LTP)
						archivo.write(escribir[0]+","+escribir[1]+","+escribir[2]+","+escribir[3]+"\n")
					archivo.write("\n"+j+",R1,R2,R3\n")
					for k in tamEnlace:
						escribir=[k]
						for l in reglas:
							arch=open(ejemplo_dir3+"\\"+k+"\\ExperimentosCooperadores\\"+l+"\\"+p+"\\"+i+"\\datos-promedio.csv","r")
							lineas=arch.readlines()
							arch.close()
							CAP,LTP,DIAM,ORCG,ATTR,ASSORT=lineas[29].replace("\n","").split(",")
							lineaLista=[CAP,LTP,DIAM,ORCG,ATTR]
							escribir.append(lineaLista[contador])
						archivo.write(escribir[0]+","+escribir[1]+","+escribir[2]+","+escribir[3]+"\n")
					archivo.write("\n"+"LTP"+",R1,R2,R3\n")
					for k in tamEnlace:
						escribir=[k]
						for l in reglas:
							arch=open(ejemplo_dir3+"\\"+k+"\\ExperimentosCooperadores\\"+l+"\\"+p+"\\"+i+"\\datos-promedio.csv","r")
							lineas=arch.readlines()
							arch.close()
							CAP,LTP,DIAM,ORCG,ATTR,ASSORT=lineas[29].replace("\n","").split(",")
							escribir.append(LTP)
						archivo.write(escribir[0]+","+escribir[1]+","+escribir[2]+","+escribir[3]+"\n")
		archivo.close()
#experimentos semi-cooperadores:
tamEnlace=["D","D2","D4","D8"]
reglas=["R1","R2","R3"]
topologias=["anillo1500","malla50x50"]
limitaciones=["n4","n16","n64"]
medidas=["CAP","LTP","DIAM","GRADO_MAX","ATTR"]
for p in topologias:
	for i in limitaciones:
		archivo=open("SemiCoop-"+p+"-"+i+".csv","w")
		for contador,j in enumerate(medidas):
			archivo.write("\n"+j+",R1,R2,R3\n")
			if contador<3:
				for k in tamEnlace:
					escribir=[k+","]
					for l in reglas:
						try:
							arch=open(ejemplo_dir+"\\"+k+"\\ExperimentosSemi-Cooperadores\\"+l+"\\"+p+"\\SP\\"+i+"\\datos-promedio.csv","r")
							lineas=arch.readlines()
							arch.close()
							CAP,LTP,DIAM,a,b,c=lineas[len(lineas)-1].replace("\n","").split(",")
							lineaLista=[CAP,LTP,DIAM]
							escribir.append(lineaLista[contador]+",")
						except FileNotFoundError as error:
							escribir.append(",")
					for contador2,w in enumerate(escribir):
						if contador2!=len(escribir)-1:
							archivo.write(escribir[contador2])
						else:
							archivo.write(escribir[contador2]+"\n")
			else:
				if contador==3:
					for k in tamEnlace:
						escribir=[k+","]
						for l in reglas:
							try:
								arch=open(ejemplo_dir+"\\"+k+"\\ExperimentosSemi-Cooperadores\\"+l+"\\"+p+"\\SP\\"+i+"\\datos-promedio_grados.csv","r")
								lineas=arch.readlines()
								arch.close()
								escribir.append(str(len(lineas)-1)+",")
							except FileNotFoundError as error:
								escribir.append(",")
						for contador2,w in enumerate(escribir):
							if contador2!=len(escribir)-1:
								archivo.write(escribir[contador2])
							else:
								archivo.write(escribir[contador2]+"\n")
				else:
					for k in tamEnlace:
						escribir=[k+","]
						for l in reglas:
							try:
								arch=open(ejemplo_dir2+"\\"+k+"\\ExperimentosSemi-Cooperadores\\"+l+"\\"+p+"\\SP\\"+i+"\\datos-promedio.csv","r")
								lineas=arch.readlines()
								arch.close()
								CAP,LTP,DIAM,ORCG,ATTR,ASSORT=lineas[29].replace("\n","").split(",")
								lineaLista=[CAP,LTP,DIAM,ORCG,ATTR]
								escribir.append(lineaLista[contador]+",")
							except FileNotFoundError as error:
								escribir.append(",")
						for contador2,w in enumerate(escribir):
							if contador2!=len(escribir)-1:
								archivo.write(escribir[contador2])
							else:
								archivo.write(escribir[contador2]+"\n")
					archivo.write("\n"+"LTP"+",R1,R2,R3\n")
					for k in tamEnlace:
						escribir=[k+","]
						for l in reglas:
							try:
								arch=open(ejemplo_dir2+"\\"+k+"\\ExperimentosSemi-Cooperadores\\"+l+"\\"+p+"\\SP\\"+i+"\\datos-promedio.csv","r")
								lineas=arch.readlines()
								arch.close()
								CAP,LTP,DIAM,ORCG,ATTR,ASSORT=lineas[29].replace("\n","").split(",")
								escribir.append(LTP+",")
							except FileNotFoundError as error:
								escribir.append(",")
						for contador2,w in enumerate(escribir):
							if contador2!=len(escribir)-1:
								archivo.write(escribir[contador2])
							else:
								archivo.write(escribir[contador2]+"\n")
					archivo.write("\n"+j+",R1,R2,R3\n")
					for k in tamEnlace:
						escribir=[k+","]
						for l in reglas:
							try:
								arch=open(ejemplo_dir3+"\\"+k+"\\ExperimentosSemi-Cooperadores\\"+l+"\\"+p+"\\SP\\"+i+"\\datos-promedio.csv","r")
								lineas=arch.readlines()
								arch.close()
								CAP,LTP,DIAM,ORCG,ATTR,ASSORT=lineas[29].replace("\n","").split(",")
								lineaLista=[CAP,LTP,DIAM,ORCG,ATTR]
								escribir.append(lineaLista[contador]+",")
							except FileNotFoundError as error:
								escribir.append(",")
						for contador2,w in enumerate(escribir):
							if contador2!=len(escribir)-1:
								archivo.write(escribir[contador2])
							else:
								archivo.write(escribir[contador2]+"\n")
					archivo.write("\n"+"LTP"+",R1,R2,R3\n")
					for k in tamEnlace:
						escribir=[k+","]
						for l in reglas:
							try:
								arch=open(ejemplo_dir3+"\\"+k+"\\ExperimentosSemi-Cooperadores\\"+l+"\\"+p+"\\SP\\"+i+"\\datos-promedio.csv","r")
								lineas=arch.readlines()
								arch.close()
								CAP,LTP,DIAM,ORCG,ATTR,ASSORT=lineas[29].replace("\n","").split(",")
								escribir.append(LTP+",")
							except FileNotFoundError as error:
								escribir.append(",")
						for contador2,w in enumerate(escribir):
							if contador2!=len(escribir)-1:
								archivo.write(escribir[contador2])
							else:
								archivo.write(escribir[contador2]+"\n")
		archivo.close()

#tamaños de enlaces vs algoritmos de encaminamiento
#experimentos cooperadores:
tamEnlace=["D","D2","D4","D8","D16"]
reglas=["R1","R2","R3"]
topologias=["anillo1500","malla50x50"]
algEncam=["CR","RW","SP"]
medidas=["CAP","LTP","DIAM","GRADO_MAX","ATTR"]
for p in topologias:
	for l in reglas:
		archivo=open("Coop_2-"+p+"-"+l+".csv","w")
		for contador,j in enumerate(medidas):
			archivo.write("\n"+j+",CR,RW,SP\n")
			if contador<3:
				for k in tamEnlace:
					escribir=[k]
					for i in algEncam:
						arch=open(ejemplo_dir+"\\"+k+"\\ExperimentosCooperadores\\"+l+"\\"+p+"\\"+i+"\\datos-promedio.csv","r")
						lineas=arch.readlines()
						arch.close()
						CAP,LTP,DIAM,a,b,c=lineas[len(lineas)-1].replace("\n","").split(",")
						lineaLista=[CAP,LTP,DIAM]
						escribir.append(lineaLista[contador])
					archivo.write(escribir[0]+","+escribir[1]+","+escribir[2]+","+escribir[3]+"\n")
			else:
				if contador==3:
					for k in tamEnlace:
						escribir=[k]
						for i in algEncam:
							arch=open(ejemplo_dir+"\\"+k+"\\ExperimentosCooperadores\\"+l+"\\"+p+"\\"+i+"\\datos-promedio_grados.csv","r")
							lineas=arch.readlines()
							arch.close()
							escribir.append(str(len(lineas)-1))
						archivo.write(escribir[0]+","+escribir[1]+","+escribir[2]+","+escribir[3]+"\n")
				else:
					for k in tamEnlace:
						escribir=[k]
						for i in algEncam:
							arch=open(ejemplo_dir2+"\\"+k+"\\ExperimentosCooperadores\\"+l+"\\"+p+"\\"+i+"\\datos-promedio.csv","r")
							lineas=arch.readlines()
							arch.close()
							CAP,LTP,DIAM,ORCG,ATTR,ASSORT=lineas[29].replace("\n","").split(",")
							lineaLista=[CAP,LTP,DIAM,ORCG,ATTR]
							escribir.append(lineaLista[contador])
						archivo.write(escribir[0]+","+escribir[1]+","+escribir[2]+","+escribir[3]+"\n")
					archivo.write("\n"+"LTP"+",CR,RW,SP\n")
					for k in tamEnlace:
						escribir=[k]
						for i in algEncam:
							arch=open(ejemplo_dir2+"\\"+k+"\\ExperimentosCooperadores\\"+l+"\\"+p+"\\"+i+"\\datos-promedio.csv","r")
							lineas=arch.readlines()
							arch.close()
							CAP,LTP,DIAM,ORCG,ATTR,ASSORT=lineas[29].replace("\n","").split(",")
							escribir.append(LTP)
						archivo.write(escribir[0]+","+escribir[1]+","+escribir[2]+","+escribir[3]+"\n")
					archivo.write("\n"+j+",CR,RW,SP\n")
					for k in tamEnlace:
						escribir=[k]
						for i in algEncam:
							arch=open(ejemplo_dir3+"\\"+k+"\\ExperimentosCooperadores\\"+l+"\\"+p+"\\"+i+"\\datos-promedio.csv","r")
							lineas=arch.readlines()
							arch.close()
							CAP,LTP,DIAM,ORCG,ATTR,ASSORT=lineas[29].replace("\n","").split(",")
							lineaLista=[CAP,LTP,DIAM,ORCG,ATTR]
							escribir.append(lineaLista[contador])
						archivo.write(escribir[0]+","+escribir[1]+","+escribir[2]+","+escribir[3]+"\n")
					archivo.write("\n"+"LTP"+",CR,RW,SP\n")
					for k in tamEnlace:
						escribir=[k]
						for i in algEncam:
							arch=open(ejemplo_dir3+"\\"+k+"\\ExperimentosCooperadores\\"+l+"\\"+p+"\\"+i+"\\datos-promedio.csv","r")
							lineas=arch.readlines()
							arch.close()
							CAP,LTP,DIAM,ORCG,ATTR,ASSORT=lineas[29].replace("\n","").split(",")
							escribir.append(LTP)
						archivo.write(escribir[0]+","+escribir[1]+","+escribir[2]+","+escribir[3]+"\n")
		archivo.close()
#experimentos semi-cooperadores:
tamEnlace=["D","D2","D4","D8"]
reglas=["R1","R2","R3"]
topologias=["anillo1500","malla50x50"]
limitaciones=["n4","n16","n64"]
medidas=["CAP","LTP","DIAM","GRADO_MAX","ATTR"]
for p in topologias:
	for l in reglas:
		archivo=open("SemiCoop2-"+p+"-"+l+".csv","w")
		for contador,j in enumerate(medidas):
			archivo.write("\n"+j+",n4,n16,n64\n")
			if contador<3:
				for k in tamEnlace:
					escribir=[k+","]
					for i in limitaciones:
						try:
							arch=open(ejemplo_dir+"\\"+k+"\\ExperimentosSemi-Cooperadores\\"+l+"\\"+p+"\\SP\\"+i+"\\datos-promedio.csv","r")
							lineas=arch.readlines()
							arch.close()
							CAP,LTP,DIAM,a,b,c=lineas[len(lineas)-1].replace("\n","").split(",")
							lineaLista=[CAP,LTP,DIAM]
							escribir.append(lineaLista[contador]+",")
						except FileNotFoundError as error:
							escribir.append(",")
					for contador2,w in enumerate(escribir):
						if contador2!=len(escribir)-1:
							archivo.write(escribir[contador2])
						else:
							archivo.write(escribir[contador2]+"\n")
			else:
				if contador==3:
					for k in tamEnlace:
						escribir=[k+","]
						for i in limitaciones:
							try:
								arch=open(ejemplo_dir+"\\"+k+"\\ExperimentosSemi-Cooperadores\\"+l+"\\"+p+"\\SP\\"+i+"\\datos-promedio_grados.csv","r")
								lineas=arch.readlines()
								arch.close()
								escribir.append(str(len(lineas)-1)+",")
							except FileNotFoundError as error:
								escribir.append(",")
						for contador2,w in enumerate(escribir):
							if contador2!=len(escribir)-1:
								archivo.write(escribir[contador2])
							else:
								archivo.write(escribir[contador2]+"\n")
				else:
					for k in tamEnlace:
						escribir=[k+","]
						for i in limitaciones:
							try:
								arch=open(ejemplo_dir2+"\\"+k+"\\ExperimentosSemi-Cooperadores\\"+l+"\\"+p+"\\SP\\"+i+"\\datos-promedio.csv","r")
								lineas=arch.readlines()
								arch.close()
								CAP,LTP,DIAM,ORCG,ATTR,ASSORT=lineas[29].replace("\n","").split(",")
								lineaLista=[CAP,LTP,DIAM,ORCG,ATTR]
								escribir.append(lineaLista[contador]+",")
							except FileNotFoundError as error:
								escribir.append(",")
						for contador2,w in enumerate(escribir):
							if contador2!=len(escribir)-1:
								archivo.write(escribir[contador2])
							else:
								archivo.write(escribir[contador2]+"\n")
					archivo.write("\n"+"LTP"+",n4,n16,n64\n")
					for k in tamEnlace:
						escribir=[k+","]
						for i in limitaciones:
							try:
								arch=open(ejemplo_dir2+"\\"+k+"\\ExperimentosSemi-Cooperadores\\"+l+"\\"+p+"\\SP\\"+i+"\\datos-promedio.csv","r")
								lineas=arch.readlines()
								arch.close()
								CAP,LTP,DIAM,ORCG,ATTR,ASSORT=lineas[29].replace("\n","").split(",")
								escribir.append(LTP+",")
							except FileNotFoundError as error:
								escribir.append(",")
						for contador2,w in enumerate(escribir):
							if contador2!=len(escribir)-1:
								archivo.write(escribir[contador2])
							else:
								archivo.write(escribir[contador2]+"\n")
					archivo.write("\n"+j+",n4,n16,n64\n")
					for k in tamEnlace:
						escribir=[k+","]
						for i in limitaciones:
							try:
								arch=open(ejemplo_dir3+"\\"+k+"\\ExperimentosSemi-Cooperadores\\"+l+"\\"+p+"\\SP\\"+i+"\\datos-promedio.csv","r")
								lineas=arch.readlines()
								arch.close()
								CAP,LTP,DIAM,ORCG,ATTR,ASSORT=lineas[29].replace("\n","").split(",")
								lineaLista=[CAP,LTP,DIAM,ORCG,ATTR]
								escribir.append(lineaLista[contador]+",")
							except FileNotFoundError as error:
								escribir.append(",")
						for contador2,w in enumerate(escribir):
							if contador2!=len(escribir)-1:
								archivo.write(escribir[contador2])
							else:
								archivo.write(escribir[contador2]+"\n")
					archivo.write("\n"+"LTP"+",n4,n16,n64\n")
					for k in tamEnlace:
						escribir=[k+","]
						for i in limitaciones:
							try:
								arch=open(ejemplo_dir3+"\\"+k+"\\ExperimentosSemi-Cooperadores\\"+l+"\\"+p+"\\SP\\"+i+"\\datos-promedio.csv","r")
								lineas=arch.readlines()
								arch.close()
								CAP,LTP,DIAM,ORCG,ATTR,ASSORT=lineas[29].replace("\n","").split(",")
								escribir.append(LTP+",")
							except FileNotFoundError as error:
								escribir.append(",")
						for contador2,w in enumerate(escribir):
							if contador2!=len(escribir)-1:
								archivo.write(escribir[contador2])
							else:
								archivo.write(escribir[contador2]+"\n")
		archivo.close()