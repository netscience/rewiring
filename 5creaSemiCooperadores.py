
import os
import config_paths as paths
import config

nodos_malla = config.COLUMNS*config.ROWS
anillo=[config.NODOS_ANILLO/4,config.NODOS_ANILLO/8,config.NODOS_ANILLO/16]
malla=[nodos_malla/4,nodos_malla/8,nodos_malla/16]
datosPromedio=open("semi-cooperadores.csv","w")
datosPromedio.write("Experimento,gradoMax,n/4,n/8,n/16\n")
datosPromedio.close()
for nombre_directorio, directorios, ficheros in os.walk(paths.RESULTADOS_DIR):#recorro recursivamente un directorio
	GRADOS=[]
	if '__pycache__' in directorios:
		directorios.remove('__pycache__')
	if ("1" in directorios and "2" in directorios and "3" in directorios and "Semi" not in nombre_directorio):#donde encuentre los directorios de las 3 ejecuciones:
		for contador,direc in enumerate(directorios):
			archivo=open(nombre_directorio+"/"+str(contador+1)+"/datos-salida_"+str(contador+1)+".txt","r")
			lineas=archivo.readlines()
			archivo.close()
			ciclo,AVCL,components,diam,APL,order = lineas[len(lineas)-1].split("\t")
			primero=open(nombre_directorio+"/"+str(contador+1)+"/hist_test_"+ciclo+".txt","r")
			lineasPrimero = primero.readlines()
			primero.close()
			grado,cantidad = lineasPrimero[len(lineasPrimero)-1].split("\t")
			GRADOS.append(float(grado))
		gradoMedio=0
		for i in GRADOS:
			gradoMedio+=i
		gradoMedio/=len(GRADOS)
		datosPromedio=open("semi-cooperadores.csv","a")
		resultados=[str(round(gradoMedio,4))]
		#Indica SI el grado promedio es mayor que 3 veces nodos/{4, 8, 16}
		if "anillo" in nombre_directorio:
			for j in anillo:
				if gradoMedio/j>=3:
					resultados.append("SI")
				else:
					resultados.append("NO")
		else:
			for j in malla:
				#print("Grado medio: ", gradoMedio)
				#print("Grado medio / j: ", gradoMedio/j)
				if gradoMedio/j>=3:
					resultados.append("SI")
				else:
					resultados.append("NO")
		datosPromedio.write(nombre_directorio.replace(paths.RESULTADOS_DIR,"")+","+resultados[0]+","+resultados[1]+","+resultados[2]+","+resultados[3]+"\n")
		datosPromedio.close()