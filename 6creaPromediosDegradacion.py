#NOTA: el separador en linux es / y en windows es \\
#NOTA: WINDOWS NO ES CASE-SENSITIVE Y LINUX SI
#NOTA: ESTE ARCHIVO SE EJECUTA EN LINUX

import os
import networkx as nx
import networkx.algorithms.community as nx_comm
import numpy as np

def getA2TR(G):
	N = nx.number_of_nodes(G)
	components = nx.connected_components(G)
	sum = 0
	for ci in components:
		Ki = len(ci)
		sum += Ki*(Ki-1)
	return sum/(N*(N-1))

def loadSequence(sFile):
	"""Reads de failure sequence and return a the sequence in list format"""
	sequence = []
	with open(sFile) as file:
		lines = file.readlines()
		for line in lines:
			sequence.append(int(line))
	return sequence

if __name__ == "__main__":
	ejemplo_dir = 'Degradación'#este es el directorio que recorrere recursivamente
	for nombre_directorio, directorios, ficheros in os.walk(ejemplo_dir):#recorro recursivamente un directorio
		if ("1" in directorios and "2" in directorios and "3" in directorios):
			print(nombre_directorio)
			ATTRs=[]
			MUATTRs=[]
			AVCLUSTs=[]
			ASSORTs=[]
			APLs=[]
			DIAMETERs=[]
			RELATIVE_ORDERs=[]
			MODULARITYs=[]
			for contador,direc in enumerate(directorios):
				archivo=open(nombre_directorio+"/"+str(contador+1)+"/degradationData.txt","r")
				lineas=archivo.readlines()
				archivo.close()
				AVCLUST_1=[]
				ASSORT1=[]
				APL_1=[]
				DIAMETER_1=[]
				ORDEN_RELATIVO_CG_1=[]
				for i,linea in enumerate(lineas):
					if i!=0:#evito la linea de los titulos
						n_nodes, m_edges, APL, diam, AVCL, assort, n_conn, n_comp, o_largestc=linea.split()
						AVCLUST_1.append(float(AVCL))
						APL_1.append(float(APL))
						DIAMETER_1.append(float(diam))
						if assort!="na":
							ASSORT1.append(float(assort))
						else:
							ASSORT1.append(999999)
						ORDEN_RELATIVO_CG_1.append(float(o_largestc)/float(n_nodes))
				#calculo los ATTR
				MUATTR=[]
				MUATTR_TOTAL=0
				ATTR_1=[]
				contenido=os.listdir(nombre_directorio+"/"+str(contador+1)+"/")
				for k in contenido:
					if ".adjlist" in k:
						G=nx.read_adjlist(nombre_directorio+"/"+str(contador+1)+"/"+k,comments='#',nodetype=int)
						orden=G.order()#orden del grafo
						MODULARIDAD1=nx_comm.modularity(G, nx_comm.louvain_communities(G))
						for j in contenido:
							if "Sequence" in j:
								degSequence = loadSequence(nombre_directorio+"/"+str(contador+1)+"/"+j)
						fallenNodes = 0 
						for i in range(len(degSequence)):
							a2tr=getA2TR(G)
							if ((fallenNodes%(orden/100))==0): 
								ATTR_1.append(a2tr)
							G.remove_node(degSequence[i])
							fallenNodes+=1
							#attr para el muATTR:
							MUATTR.append(a2tr)
						#calculo el muATTR
						for i in MUATTR:
							MUATTR_TOTAL+=i
						MUATTR_TOTAL=MUATTR_TOTAL/(orden-1)
				MUATTRs.append(MUATTR_TOTAL)
				MODULARITYs.append(MODULARIDAD1)
				AVCLUSTs.append(AVCLUST_1)
				ASSORTs.append(ASSORT1)
				APLs.append(APL_1)
				DIAMETERs.append(DIAMETER_1)
				RELATIVE_ORDERs.append(ORDEN_RELATIVO_CG_1)
				ATTRs.append(ATTR_1)
			#calculo los promedios de los elementos de las listas:
			AVCL_AVERAGE=[]
			APL_AVERAGE=[]
			DIAMETER_AVERAGE=[]
			ASSORT_AVERAGE=[]
			ORDEN_RELATIVO_CG_AVERAGE=[]
			ATTR_AVERAGE=[]
			for i in range(len(AVCLUSTs[0])):
				AVCL_AVG=0
				APL_AVG=0
				DIAM_AVG=0
				ASS_AVG=0
				ROGC_AVG=0
				ATTR_AVG=0
				for j in range(len(AVCLUSTs)):
					AVCL_AVG+=AVCLUSTs[j][i]
					APL_AVG+=APLs[j][i]
					DIAM_AVG+=DIAMETERs[j][i]
					ASS_AVG+=ASSORTs[j][i]
					ROGC_AVG+=RELATIVE_ORDERs[j][i]
					try:
						ATTR_AVG+=ATTRs[j][i]
					except:
						pass
				AVCL_AVERAGE.append(AVCL_AVG/len(AVCLUSTs))
				APL_AVERAGE.append(APL_AVG/len(AVCLUSTs))
				ASSORT_AVERAGE.append(ASS_AVG/len(AVCLUSTs))
				DIAMETER_AVERAGE.append(DIAM_AVG/len(AVCLUSTs))
				ORDEN_RELATIVO_CG_AVERAGE.append(ROGC_AVG/len(AVCLUSTs))
				ATTR_AVERAGE.append(ATTR_AVG/len(AVCLUSTs))
			datosPromedio=open(nombre_directorio+"/datos-promedio.csv","w")
			for i in range(len(AVCLUST_1)):
				datosPromedio.write('{0:.6f},'.format(AVCL_AVERAGE[i]))
				datosPromedio.write('{0:.6f},'.format(APL_AVERAGE[i]))
				datosPromedio.write('{0:.6f},'.format(DIAMETER_AVERAGE[i]))
				datosPromedio.write('{0:.6f},'.format(ORDEN_RELATIVO_CG_AVERAGE[i]))
				datosPromedio.write('{0:.6f},'.format(ATTR_AVERAGE[i]))
				datosPromedio.write('{0:.6f}\n'.format(ASSORT_AVERAGE[i]))
			MUA2TR=np.mean(MUATTRs)
			MUA2TRstd=np.std(MUATTRs)
			MODULARIDAD=np.mean(MODULARITYs)
			MODULARIDADstd=np.std(MODULARITYs)
			datosPromedio.write(',,,,{0:.6f}\n'.format(MUA2TR))
			datosPromedio.write(',,,,{0:.6f}\n'.format(MODULARIDAD))
			datosPromedio.write(',,,,{0:.6f}\n'.format(MUA2TRstd))
			datosPromedio.write(',,,,{0:.6f}\n'.format(MODULARIDADstd))
			datosPromedio.close()
