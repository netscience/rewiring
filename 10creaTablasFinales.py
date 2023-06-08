
from random import uniform,random
import os
from math import ceil
import matplotlib.pyplot as plt
import numpy as np
import networkx as nx

ejemplo_dir = 'C:\\Users\\VG\\Documents\\Formación'#este es el directorio que recorrere recursivamente
muestrasAnillo=[]
muestrasMalla=[]
for nombre_directorio, subdirectorios, ficheros in os.walk(ejemplo_dir):#recorro recursivamente un directorio
	if("1" in subdirectorios and "2" in subdirectorios and "3" in subdirectorios):
		primero=open(nombre_directorio+"\\datos-promedio.csv","r")
		lineasPrimero = primero.readlines()
		primero.close()
		AVCL,LTP,DIAM,AVCLstd,LTPstd,DIAMstd = lineasPrimero[len(lineasPrimero)-1].split(",")
		#calculo el ciclo en que se estabilizan las metricas
		#para el AVCL:
		diferencias=[]
		for contador,linea in enumerate(lineasPrimero):
			AVCL_I,LTP_I,DIAM_I,a,b,c = lineasPrimero[contador].split(",")
			diferencias.append(abs(float(AVCL)-float(AVCL_I)))
		ciclosCumplen=[]
		for i in range(len(diferencias)-1,0,-1):
			if diferencias[i]<0.01:
				ciclosCumplen.append(i)
			else:
				break
		cicloEstableAVCL=ciclosCumplen[len(ciclosCumplen)-1]
		#para la LTP:
		diferencias=[]
		for contador,linea in enumerate(lineasPrimero):
			AVCL_I,LTP_I,DIAM_I,a,b,c = lineasPrimero[contador].split(",")
			diferencias.append(abs(float(LTP)-float(LTP_I)))
		ciclosCumplen=[]
		for i in range(len(diferencias)-1,0,-1):
			if diferencias[i]<1.1:
				ciclosCumplen.append(i)
			else:
				break
		cicloEstableLTP=ciclosCumplen[len(ciclosCumplen)-1]
		#para el DIAM:
		diferencias=[]
		for contador,linea in enumerate(lineasPrimero):
			AVCL_I,LTP_I,DIAM_I,a,b,c = lineasPrimero[contador].split(",")
			diferencias.append(abs(float(DIAM)-float(DIAM_I)))
		ciclosCumplen=[]
		for i in range(len(diferencias)-1,0,-1):
			if diferencias[i]<1.1:
				ciclosCumplen.append(i)
			else:
				break
		cicloEstableDIAM=ciclosCumplen[len(ciclosCumplen)-1]
		tams=[]
		maxs=[]
		mins=[]
		medias=[]
		stddevs=[]
		#calculo grado medio, desviacion estandar, grado minimo y grado maximo
		for i in range(1,11):
			primero=open(nombre_directorio+"\\"+str(i)+"\\datos-salida_"+str(i)+".txt","r")
			lineasPrimero = primero.readlines()
			primero.close()
			ciclo1,avcl,components,diam,APL,order = lineasPrimero[len(lineasPrimero)-1].split("\t")
			G = nx.read_adjlist(nombre_directorio+"\\"+str(i)+"\\graph_test_"+ciclo1+".adjlist", nodetype=int)
			tams.append(G.size())
			f=open(nombre_directorio+"\\"+str(i)+"\\hist_test_"+ciclo1+".txt","r")#obtengo los datos del archivo txt
			lines=f.readlines()
			f.close()
			values1=[]
			for line in lines:
				linea=line.split("\t")
				for i in range(int(linea[1])):
					values1.append(int(linea[0]))
			muestras1=np.array(values1)
			maxs.append(max(values1))
			mins.append(min(values1))
			medias.append(np.mean(values1))
			stddevs.append(np.std(values1))
		minimo=min(mins)
		maximo=max(maxs)
		media=np.mean(medias)
		stdDev=np.mean(stddevs)
		tamano=np.mean(tams)
		if "anillo" in nombre_directorio:
			ordenGrafo=1500
		else:
			ordenGrafo=2500
		densidades=[]
		for i in tams:
			densidades.append(i/((ordenGrafo*(ordenGrafo-1))/2))
		densPro=np.mean(densidades)
		#obtengo los datos: ASSORT, MUA2TR, MODULARITY, A2TR, APL, ORCG
		direcAtaq=nombre_directorio[:]
		direcFall=nombre_directorio[:]
		direcAtaq=direcAtaq.replace("Formación","Degradación\\Ataques\\GrafosFinales")
		direcFall=direcFall.replace("Formación","Degradación\\Fallas\\GrafosFinales")
		#para ataques:
		primero=open(direcAtaq+"\\datos-promedio.csv","r")
		lineasPrimero = primero.readlines()
		primero.close()
		b1,b2,b3,b4,b5,ASSORT = lineasPrimero[0].split(",")
		b1,b2,b3,b4,MUATTR = lineasPrimero[len(lineasPrimero)-4].split(",")
		b1,b2,b3,b4,MODULARITY = lineasPrimero[len(lineasPrimero)-3].split(",")
		b1,b2,b3,b4,MUATTRstd = lineasPrimero[len(lineasPrimero)-2].split(",")
		b1,b2,b3,b4,MODULARITYstd = lineasPrimero[len(lineasPrimero)-1].split(",")
		MUATTR=round(float(MUATTR),2)
		coefAgr,APL,diameter,ORCG,A2TR,b6 = lineasPrimero[int(MUATTR*100)-1].split(",")
		#para fallas:
		primero=open(direcFall+"\\datos-promedio.csv","r")
		lineasPrimero = primero.readlines()
		primero.close()
		b1,b2,b3,b4,MUATTR2 = lineasPrimero[len(lineasPrimero)-4].split(",")
		b1,b2,b3,b4,MODULARITY2 = lineasPrimero[len(lineasPrimero)-3].split(",")
		b1,b2,b3,b4,MUATTRstd2 = lineasPrimero[len(lineasPrimero)-2].split(",")
		b1,b2,b3,b4,MODULARITYstd2 = lineasPrimero[len(lineasPrimero)-1].split(",")
		MUATTR2=round(float(MUATTR2),2)
		coefAgr2,APL2,diameter2,ORCG2,A2TR2,b6 = lineasPrimero[int(MUATTR2*100)-1].split(",")
		muestra=[nombre_directorio.replace("C:\\Users\\VG\\Documents\\Formación\\","").replace("Experimentos","").replace("Cooperadores","Coop"),round(float(tamano),3),round(float(densPro),3),round(float(minimo),3),round(float(maximo),3),round(float(media),3),round(float(stdDev),3),round(float(AVCL),3),round(float(AVCLstd),3),round(float(cicloEstableAVCL),3),round(float(LTP),3),round(float(LTPstd),3),round(float(cicloEstableLTP),3),round(float(DIAM),3),round(float(DIAMstd.replace("\n","")),3),round(float(cicloEstableDIAM),3),round(float(MODULARITY.replace("\n","")),3),round(float(MODULARITYstd.replace("\n","")),3),round(float(ASSORT.replace("\n","")),3),MUATTR,round(float(MUATTRstd.replace("\n","")),3),round(float(A2TR),3),round(float(ORCG),3),round(float(APL),3),round(float(diameter),3),MUATTR2,round(float(MUATTRstd2.replace("\n","")),3),round(float(A2TR2),3),round(float(ORCG2),3),round(float(APL2),3),round(float(diameter2),3)]
		if "anillo" in nombre_directorio:
			muestrasAnillo.append(muestra)
		else:
			muestrasMalla.append(muestra)
#escribo las muestras del anillo en un CSV
with open("anillo.csv", "w", encoding="utf-8") as muestras:
	muestras.write("Configuration,|E|,Den,MinDeg,MaxDeg,AvgDeg,SD,AVCL,SD,SC,APL,SD,SC,Diam,SD,SC,Mod,SD,Assor,muA2TR,SD,A2TR,ROGC,APL,Diam,muA2TR,SD,A2TR,ROGC,APL,Diam\n")
	for i in range(len(muestrasAnillo)):
		muestras.write(str(muestrasAnillo[i][0]).replace("\\anillo1500","")+","+str(muestrasAnillo[i][1])+","+str(muestrasAnillo[i][2])+","+str(muestrasAnillo[i][3])+","+str(muestrasAnillo[i][4])+","+str(muestrasAnillo[i][5])+","+str(muestrasAnillo[i][6])+","+str(muestrasAnillo[i][7])+","+str(muestrasAnillo[i][8])+","+str(muestrasAnillo[i][9])+","+str(muestrasAnillo[i][10])+","+str(muestrasAnillo[i][11])+","+str(muestrasAnillo[i][12])+","+str(muestrasAnillo[i][13])+","+str(muestrasAnillo[i][14])+","+str(muestrasAnillo[i][15])+","+str(muestrasAnillo[i][16])+","+str(muestrasAnillo[i][17])+","+str(muestrasAnillo[i][18])+","+str(muestrasAnillo[i][19])+","+str(muestrasAnillo[i][20])+","+str(muestrasAnillo[i][21])+","+str(muestrasAnillo[i][22])+","+str(muestrasAnillo[i][23])+","+str(muestrasAnillo[i][24])+","+str(muestrasAnillo[i][25])+","+str(muestrasAnillo[i][26])+","+str(muestrasAnillo[i][27])+","+str(muestrasAnillo[i][28])+","+str(muestrasAnillo[i][29])+","+str(muestrasAnillo[i][30])+"\n")
#escribo las muestras de la malla en un CSV
with open("malla.csv", "w", encoding="utf-8") as muestras:
	muestras.write("Configuration,|E|,Den,MinDeg,MaxDeg,AvgDeg,SD,AVCL,SD,SC,APL,SD,SC,Diam,SD,SC,Mod,SD,Assor,muA2TR,SD,A2TR,ROGC,APL,Diam,muA2TR,SD,A2TR,ROGC,APL,Diam\n")
	for i in range(len(muestrasMalla)):
		muestras.write(str(muestrasMalla[i][0]).replace("\\malla50x50","")+","+str(muestrasMalla[i][1])+","+str(muestrasMalla[i][2])+","+str(muestrasMalla[i][3])+","+str(muestrasMalla[i][4])+","+str(muestrasMalla[i][5])+","+str(muestrasMalla[i][6])+","+str(muestrasMalla[i][7])+","+str(muestrasMalla[i][8])+","+str(muestrasMalla[i][9])+","+str(muestrasMalla[i][10])+","+str(muestrasMalla[i][11])+","+str(muestrasMalla[i][12])+","+str(muestrasMalla[i][13])+","+str(muestrasMalla[i][14])+","+str(muestrasMalla[i][15])+","+str(muestrasMalla[i][16])+","+str(muestrasMalla[i][17])+","+str(muestrasMalla[i][18])+","+str(muestrasMalla[i][19])+","+str(muestrasMalla[i][20])+","+str(muestrasMalla[i][21])+","+str(muestrasMalla[i][22])+","+str(muestrasMalla[i][23])+","+str(muestrasMalla[i][24])+","+str(muestrasMalla[i][25])+","+str(muestrasMalla[i][26])+","+str(muestrasMalla[i][27])+","+str(muestrasMalla[i][28])+","+str(muestrasMalla[i][29])+","+str(muestrasMalla[i][30])+"\n")