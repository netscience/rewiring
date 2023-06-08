
import os
import numpy as np

ejemplo_dir = 'C:\\Users\\VG\\Documents\\Formación'#este es el directorio que recorrere recursivamente

for nombre_directorio, directorios, ficheros in os.walk(ejemplo_dir):#recorro recursivamente un directorio
	AVCLUSTs=[]
	APLs=[]
	DIAMETERs=[]
	if ("1" in directorios and "2" in directorios and "3" in directorios):
		for contador,direc in enumerate(directorios):
			archivo=open(nombre_directorio+"\\"+str(contador+1)+"\\datos-salida_"+str(contador+1)+".txt","r")
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
			#verifico que se hayan terminado los 50 ciclos en el archivo:
			if len(AVCLUST_1)<51:
				#si no se ejecutaron los 50 ciclos repito los datos del ultimo ciclo ejecutado hasta completar los 50 ciclos:
				faltantes=51-len(AVCLUST_1)
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
		for i in range(51):
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
		datosPromedio=open(nombre_directorio+"\\datos-promedio.csv","w")
		for i in range(51):
			datosPromedio.write('{0:.3f},'.format(AVCL_AVERAGE[i]))
			datosPromedio.write('{0:.3f},'.format(APL_AVERAGE[i]))
			datosPromedio.write('{0:.3f},'.format(DIAMETER_AVERAGE[i]))
			datosPromedio.write('{0:.3f},'.format(STDAVCL[i]))
			datosPromedio.write('{0:.3f},'.format(STDAPL[i]))
			datosPromedio.write('{0:.3f}\n'.format(STDDIAM[i]))
		datosPromedio.close()