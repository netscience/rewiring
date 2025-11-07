import configVisualizacion
import configPaths

#crea un resumen de las medidas promedio obtenidas previamente de la parte de formacion y degradacion de redes complejas

#tamaños de enlaces vs reglas de recableado
#experimentos cooperadores:
ejemplo_dir2 = configPaths.DEGRADACION_DIR + '/Ataques/GrafosFinales'
ejemplo_dir3 = configPaths.DEGRADACION_DIR + '/Fallas/GrafosFinales'
tamEnlace=configVisualizacion.TAM_ENLACES
reglas=configVisualizacion.REGLAS
topologias=configVisualizacion.TOPOLOGIAS
algEncam=configVisualizacion.ALG_ENCAMINAMIENTO
medidas=["CAP","LTP","DIAM","GRADO_MAX","ATTR"]
for p in topologias:
	for i in algEncam:
		archivo=open("Coop-"+p+"-"+i+".csv","w")
		for contador,j in enumerate(medidas):
			archivo.write("\n"+j+configVisualizacion.COLS_REGLAS+"\n")
			if contador<3:
				for k in tamEnlace:
					escribir=[k]
					for l in reglas:
						arch=open(configPaths.RESULTADOS_DIR+"/"+k+"/ExperimentosCooperadores/"+l+"/"+p+"/"+i+"/datos-promedio.csv","r")
						lineas=arch.readlines()
						arch.close()
						ciclo,CAP,LTP,DIAM,a,b,c=lineas[len(lineas)-1].replace("\n","").split(",")
						lineaLista=[CAP,LTP,DIAM]
						escribir.append(lineaLista[contador])
					if len(reglas) == 1:
						archivo.write(escribir[0]+","+escribir[1]+"\n")
					elif len(reglas) == 2:
						archivo.write(escribir[0]+","+escribir[1]+","+escribir[2]+"\n")
					else:
						archivo.write(escribir[0]+","+escribir[1]+","+escribir[2]+","+escribir[3]+"\n")
			else:
				if contador==3:
					for k in tamEnlace:
						escribir=[k]
						for l in reglas:
							arch=open(configPaths.RESULTADOS_DIR+"/"+k+"/ExperimentosCooperadores/"+l+"/"+p+"/"+i+"/datos-promedio_grados.csv","r")
							lineas=arch.readlines()
							arch.close()
							escribir.append(str(len(lineas)-1))
						if len(reglas) == 1:
							archivo.write(escribir[0]+","+escribir[1]+"\n")
						elif len(reglas) == 2:
							archivo.write(escribir[0]+","+escribir[1]+","+escribir[2]+"\n")
						else:
							archivo.write(escribir[0]+","+escribir[1]+","+escribir[2]+","+escribir[3]+"\n")
				else:
					for k in tamEnlace:
						escribir=[k]
						for l in reglas:
							arch=open(ejemplo_dir2+"/"+k+"/ExperimentosCooperadores/"+l+"/"+p+"/"+i+"/datos-promedio.csv","r")
							lineas=arch.readlines()
							arch.close()
							print(ejemplo_dir2+"/"+k+"/ExperimentosCooperadores/"+l+"/"+p+"/"+i+"/datos-promedio.csv")
							CAP,LTP,DIAM,ORCG,ASSORT=lineas[-1].replace("\n","").split(",")
							lineaLista=[CAP,LTP,DIAM,ORCG]
							escribir.append(lineaLista[contador])
						archivo.write(escribir[0]+","+escribir[1]+","+escribir[2]+","+escribir[3]+"\n")
					archivo.write("\n"+"LTP"+","+configVisualizacion.COLS_REGLAS+"\n")
					for k in tamEnlace:
						escribir=[k]
						for l in reglas:
							arch=open(ejemplo_dir2+"/"+k+"/ExperimentosCooperadores/"+l+"/"+p+"/"+i+"/datos-promedio.csv","r")
							lineas=arch.readlines()
							arch.close()
							CAP,LTP,DIAM,ORCG,ATTR,ASSORT=lineas[29].replace("\n","").split(",")
							escribir.append(LTP)
						archivo.write(escribir[0]+","+escribir[1]+","+escribir[2]+","+escribir[3]+"\n")
					archivo.write("\n"+j+","+configVisualizacion.COLS_REGLAS+"\n")
					for k in tamEnlace:
						escribir=[k]
						for l in reglas:
							arch=open(ejemplo_dir3+"/"+k+"/ExperimentosCooperadores/"+l+"/"+p+"/"+i+"/datos-promedio.csv","r")
							lineas=arch.readlines()
							arch.close()
							CAP,LTP,DIAM,ORCG,ATTR,ASSORT=lineas[29].replace("\n","").split(",")
							lineaLista=[CAP,LTP,DIAM,ORCG,ATTR]
							escribir.append(lineaLista[contador])
						archivo.write(escribir[0]+","+escribir[1]+","+escribir[2]+","+escribir[3]+"\n")
					archivo.write("\n"+"LTP"+","+configVisualizacion.COLS_REGLAS+"\n")
					for k in tamEnlace:
						escribir=[k]
						for l in reglas:
							arch=open(ejemplo_dir3+"/"+k+"/ExperimentosCooperadores/"+l+"/"+p+"/"+i+"/datos-promedio.csv","r")
							lineas=arch.readlines()
							arch.close()
							CAP,LTP,DIAM,ORCG,ATTR,ASSORT=lineas[29].replace("\n","").split(",")
							escribir.append(LTP)
						archivo.write(escribir[0]+","+escribir[1]+","+escribir[2]+","+escribir[3]+"\n")
		archivo.close()
#experimentos semi-cooperadores:
tamEnlace=configVisualizacion.TAM_ENLACES_SC
reglas=configVisualizacion.REGLAS_SC
topologias=configVisualizacion.TOPOLOGIAS_SC
limitaciones=configVisualizacion.CONEXIONES_SC
medidas=["CAP","LTP","DIAM","GRADO_MAX","ATTR"]
for p in topologias:
	for i in limitaciones:
		archivo=open("SemiCoop-"+p+"-"+i+".csv","w")
		for contador,j in enumerate(medidas):
			archivo.write("\n"+j+","+configVisualizacion.COLS_REGLAS+"\n")
			if contador<3:
				for k in tamEnlace:
					escribir=[k+","]
					for l in reglas:
						try:
							arch=open(configPaths.RESULTADOS_DIR+"/"+k+"/ExperimentosSemi-Cooperadores/"+l+"/"+p+"/SP/"+i+"/datos-promedio.csv","r")
							lineas=arch.readlines()
							arch.close()
							CAP,LTP,DIAM,a,b=lineas[len(lineas)-1].replace("\n","").split(",")
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
								arch=open(configPaths.RESULTADOS_DIR+"/"+k+"/ExperimentosSemi-Cooperadores/"+l+"/"+p+"/SP/"+i+"/datos-promedio_grados.csv","r")
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
								arch=open(ejemplo_dir2+"/"+k+"/ExperimentosSemi-Cooperadores/"+l+"/"+p+"/SP/"+i+"/datos-promedio.csv","r")
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
					archivo.write("\n"+"LTP"+","+configVisualizacion.COLS_REGLAS+"\n")
					for k in tamEnlace:
						escribir=[k+","]
						for l in reglas:
							try:
								arch=open(ejemplo_dir2+"/"+k+"/ExperimentosSemi-Cooperadores/"+l+"/"+p+"/SP/"+i+"/datos-promedio.csv","r")
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
					archivo.write("\n"+j+","+configVisualizacion.COLS_REGLAS+"\n")
					for k in tamEnlace:
						escribir=[k+","]
						for l in reglas:
							try:
								arch=open(ejemplo_dir3+"/"+k+"/ExperimentosSemi-Cooperadores/"+l+"/"+p+"/SP/"+i+"/datos-promedio.csv","r")
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
					archivo.write("\n"+"LTP"+","+configVisualizacion.COLS_REGLAS+"\n")
					for k in tamEnlace:
						escribir=[k+","]
						for l in reglas:
							try:
								arch=open(ejemplo_dir3+"/"+k+"/ExperimentosSemi-Cooperadores/"+l+"/"+p+"/SP/"+i+"/datos-promedio.csv","r")
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
tamEnlace=configVisualizacion.TAM_ENLACES
reglas=configVisualizacion.REGLAS
topologias=configVisualizacion.TOPOLOGIAS
algEncam=configVisualizacion.ALG_ENCAMINAMIENTO
medidas=["CAP","LTP","DIAM","GRADO_MAX","ATTR"]
for p in topologias:
	for l in reglas:
		archivo=open("Coop_2-"+p+"-"+l+".csv","w")
		for contador,j in enumerate(medidas):
			archivo.write("\n"+j+","+configVisualizacion.COLS_ROUTING+"\n")
			if contador<3:
				for k in tamEnlace:
					escribir=[k]
					for i in algEncam:
						arch=open(configPaths.RESULTADOS_DIR+"/"+k+"/ExperimentosCooperadores/"+l+"/"+p+"/"+i+"/datos-promedio.csv","r")
						lineas=arch.readlines()
						arch.close()
						CAP,LTP,DIAM,a,b=lineas[len(lineas)-1].replace("\n","").split(",")
						lineaLista=[CAP,LTP,DIAM]
						escribir.append(lineaLista[contador])
					archivo.write(escribir[0]+","+escribir[1]+","+escribir[2]+","+escribir[3]+"\n")
			else:
				if contador==3:
					for k in tamEnlace:
						escribir=[k]
						for i in algEncam:
							arch=open(configPaths.RESULTADOS_DIR+"/"+k+"/ExperimentosCooperadores/"+l+"/"+p+"/"+i+"/datos-promedio_grados.csv","r")
							lineas=arch.readlines()
							arch.close()
							escribir.append(str(len(lineas)-1))
						archivo.write(escribir[0]+","+escribir[1]+","+escribir[2]+","+escribir[3]+"\n")
				else:
					for k in tamEnlace:
						escribir=[k]
						for i in algEncam:
							arch=open(configPaths.RESULTADOS_DIR+"/"+k+"/ExperimentosCooperadores/"+l+"/"+p+"/"+i+"/datos-promedio.csv","r")
							lineas=arch.readlines()
							arch.close()
							CAP,LTP,DIAM,ORCG,ATTR,ASSORT=lineas[29].replace("\n","").split(",")
							lineaLista=[CAP,LTP,DIAM,ORCG,ATTR]
							escribir.append(lineaLista[contador])
						archivo.write(escribir[0]+","+escribir[1]+","+escribir[2]+","+escribir[3]+"\n")
					archivo.write("\n"+"LTP"+","+configVisualizacion.COLS_ROUTING+"\n")
					for k in tamEnlace:
						escribir=[k]
						for i in algEncam:
							arch=open(ejemplo_dir2+"/"+k+"/ExperimentosCooperadores/"+l+"/"+p+"/"+i+"/datos-promedio.csv","r")
							lineas=arch.readlines()
							arch.close()
							CAP,LTP,DIAM,ORCG,ATTR,ASSORT=lineas[29].replace("\n","").split(",")
							escribir.append(LTP)
						archivo.write(escribir[0]+","+escribir[1]+","+escribir[2]+","+escribir[3]+"\n")
					archivo.write("\n"+j+","+configVisualizacion.COLS_ROUTING+"\n")
					for k in tamEnlace:
						escribir=[k]
						for i in algEncam:
							arch=open(ejemplo_dir3+"/"+k+"/ExperimentosCooperadores/"+l+"/"+p+"/"+i+"/datos-promedio.csv","r")
							lineas=arch.readlines()
							arch.close()
							CAP,LTP,DIAM,ORCG,ATTR,ASSORT=lineas[29].replace("\n","").split(",")
							lineaLista=[CAP,LTP,DIAM,ORCG,ATTR]
							escribir.append(lineaLista[contador])
						archivo.write(escribir[0]+","+escribir[1]+","+escribir[2]+","+escribir[3]+"\n")
					archivo.write("\n"+"LTP"+","+configVisualizacion.COLS_ROUTING+"\n")
					for k in tamEnlace:
						escribir=[k]
						for i in algEncam:
							arch=open(ejemplo_dir3+"/"+k+"/ExperimentosCooperadores/"+l+"/"+p+"/"+i+"/datos-promedio.csv","r")
							lineas=arch.readlines()
							arch.close()
							CAP,LTP,DIAM,ORCG,ATTR,ASSORT=lineas[29].replace("\n","").split(",")
							escribir.append(LTP)
						archivo.write(escribir[0]+","+escribir[1]+","+escribir[2]+","+escribir[3]+"\n")
		archivo.close()
#experimentos semi-cooperadores:
tamEnlace=configVisualizacion.TAM_ENLACES_SC
reglas=configVisualizacion.REGLAS_SC
topologias=configVisualizacion.TOPOLOGIAS_SC
limitaciones=configVisualizacion.CONEXIONES_SC
medidas=["CAP","LTP","DIAM","GRADO_MAX","ATTR"]
for p in topologias:
	for l in reglas:
		archivo=open("SemiCoop2-"+p+"-"+l+".csv","w")
		for contador,j in enumerate(medidas):
			archivo.write("\n"+j+","+configVisualizacion.COLS_CONEXIONES+"\n")
			if contador<3:
				for k in tamEnlace:
					escribir=[k+","]
					for i in limitaciones:
						try:
							arch=open(configPaths.RESULTADOS_DIR+"/"+k+"/ExperimentosSemi-Cooperadores/"+l+"/"+p+"/SP/"+i+"/datos-promedio.csv","r")
							lineas=arch.readlines()
							arch.close()
							CAP,LTP,DIAM,a,b=lineas[len(lineas)-1].replace("\n","").split(",")
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
								arch=open(configPaths.RESULTADOS_DIR+"/"+k+"/ExperimentosSemi-Cooperadores/"+l+"/"+p+"/SP/"+i+"/datos-promedio_grados.csv","r")
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
								arch=open(ejemplo_dir2+"/"+k+"/ExperimentosSemi-Cooperadores/"+l+"/"+p+"/SP/"+i+"/datos-promedio.csv","r")
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
					archivo.write("\n"+"LTP"+","+configVisualizacion.COLS_CONEXIONES+"\n")
					for k in tamEnlace:
						escribir=[k+","]
						for i in limitaciones:
							try:
								arch=open(ejemplo_dir2+"/"+k+"/ExperimentosSemi-Cooperadores/"+l+"/"+p+"/SP/"+i+"/datos-promedio.csv","r")
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
					archivo.write("\n"+j+","+configVisualizacion.COLS_CONEXIONES+"\n")
					for k in tamEnlace:
						escribir=[k+","]
						for i in limitaciones:
							try:
								arch=open(ejemplo_dir3+"/"+k+"/ExperimentosSemi-Cooperadores/"+l+"/"+p+"/SP/"+i+"/datos-promedio.csv","r")
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
					archivo.write("\n"+"LTP"+","+configVisualizacion.COLS_CONEXIONES+"\n")
					for k in tamEnlace:
						escribir=[k+","]
						for i in limitaciones:
							try:
								arch=open(ejemplo_dir3+"/"+k+"/ExperimentosSemi-Cooperadores/"+l+"/"+p+"/SP/"+i+"/datos-promedio.csv","r")
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