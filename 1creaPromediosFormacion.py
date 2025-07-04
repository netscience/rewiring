
import os
import numpy as np
import config_paths as paths
import config

for nombre_directorio, directorios, ficheros in os.walk(paths.RESULTADOS_DIR):#recorro recursivamente un directorio
	AVCLUSTs=[]
	APLs=[]
	DIAMETERs=[]
	if '__pycache__' in directorios:
		directorios.remove('__pycache__')

	if ("1" in directorios and "2" in directorios and "3" in directorios):
		for contador,direc in enumerate(directorios):
			datos_salida = nombre_directorio+"/"+str(contador+1)+"/datos-salida_"+str(contador+1)+".txt"
			archivo=open(datos_salida,"r")
			lineas=archivo.readlines()
			archivo.close()
			AVCLUST_1=[]
			APL_1=[]
			DIAMETER_1=[]
			for i,linea in enumerate(lineas):
				if i!=0:#evito la linea de los titulos
					ciclo,AVCL,components,diam,APL,order = linea.split("\t")
					try:
						cicloSig,AVCLSig,componentsSig,diamSig,APLSig,orderSig = lineas[i+1].split("\t")
						if ciclo!=cicloSig:
							diferencia=float(cicloSig)-float(ciclo)
							while diferencia!=0:
								AVCLUST_1.append(float(AVCL))
								APL_1.append(float(APL))
								DIAMETER_1.append(float(diam))
								diferencia-=1
						else:
							AVCLUST_1.append(float(AVCL))
							APL_1.append(float(APL))
							DIAMETER_1.append(float(diam))	
					except IndexError as error:
						AVCLUST_1.append(float(AVCL))
						APL_1.append(float(APL))
						DIAMETER_1.append(float(diam))	
			#verifico que se hayan terminado todos los ciclos en el archivo:
			if len(AVCLUST_1)<config.CICLOS+1:
				#si no se ejecutaron todos los ciclos repito los datos del ultimo ciclo ejecutado hasta completar los 50 ciclos:
				faltantes=config.CICLOS+1-len(AVCLUST_1)
				AVCLUST_1_FINAL=AVCLUST_1[len(AVCLUST_1)-1]
				APL_1_FINAL=APL_1[len(APL_1)-1]
				DIAMETER_1_FINAL=DIAMETER_1[len(DIAMETER_1)-1]
				for i in range(faltantes):
					AVCLUST_1.append(AVCLUST_1_FINAL)
					APL_1.append(APL_1_FINAL)
					DIAMETER_1.append(DIAMETER_1_FINAL)
			AVCLUSTs.append(AVCLUST_1)
			APLs.append(APL_1)
			DIAMETERs.append(DIAMETER_1)
		#calculo los promedios de los elementos de las listas:
		AVCL_AVERAGE=[]
		APL_AVERAGE=[]
		DIAMETER_AVERAGE=[]
		STDAVCL=[]
		STDAPL=[]
		STDDIAM=[]
		for i in range(config.CICLOS+1):
			AVGAVCL=0
			AVGAPL=0
			AVGDIAM=0
			stdAVCL=[]
			stdAPL=[]
			stdDIAM=[]
			for j in range(len(AVCLUSTs)):
				AVGAVCL+=AVCLUSTs[j][i]
				AVGAPL+=APLs[j][i]
				AVGDIAM+=DIAMETERs[j][i]
				stdAVCL.append(AVCLUSTs[j][i])
				stdAPL.append(APLs[j][i])
				stdDIAM.append(DIAMETERs[j][i])
			AVGAVCL/=len(AVCLUSTs)
			AVGAPL/=len(AVCLUSTs)
			AVGDIAM/=len(AVCLUSTs)
			AVCL_AVERAGE.append(AVGAVCL)
			APL_AVERAGE.append(AVGAPL)
			DIAMETER_AVERAGE.append(AVGDIAM)
			STDAVCL.append(np.std(stdAVCL))
			STDAPL.append(np.std(stdAPL))
			STDDIAM.append(np.std(stdDIAM))
		datosPromedio=open(nombre_directorio+"/datos-promedio.csv","w")
		datosPromedio.write("ciclo,avCl,aslp,dia,std_avCL,std_aspl,std_dia\n")
		for i in range(config.CICLOS+1):
			datosPromedio.write(str(i)+',')
			datosPromedio.write('{0:.3f},'.format(AVCL_AVERAGE[i]))
			datosPromedio.write('{0:.3f},'.format(APL_AVERAGE[i]))
			datosPromedio.write('{0:.3f},'.format(DIAMETER_AVERAGE[i]))
			datosPromedio.write('{0:.3f},'.format(STDAVCL[i]))
			datosPromedio.write('{0:.3f},'.format(STDAPL[i]))
			datosPromedio.write('{0:.3f}\n'.format(STDDIAM[i]))
		datosPromedio.close()