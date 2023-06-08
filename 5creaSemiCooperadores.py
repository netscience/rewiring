
import os

ejemplo_dir = "C:\\Users\\VG\\Documents\\Formación"#este es el directorio que recorrere recursivamente

anillo=[1500/4,1500/16,1500/64]
malla=[2500/4,2500/16,2500/64]
datosPromedio=open("semi-cooperadores.csv","w")
datosPromedio.write("Experimento,gradoMax,n/4,n/16,n/64\n")
datosPromedio.close()
for nombre_directorio, directorios, ficheros in os.walk(ejemplo_dir):#recorro recursivamente un directorio
	GRADOS=[]
	if ("1" in directorios and "2" in directorios and "3" in directorios and "Semi" not in nombre_directorio):#donde encuentre los directorios de las 3 ejecuciones:
		for contador,direc in enumerate(directorios):
			archivo=open(nombre_directorio+"\\"+str(contador+1)+"\\datos-salida_"+str(contador+1)+".txt","r")
			lineas=archivo.readlines()
			archivo.close()
			ciclo,AVCL,components,diam,APL,order = lineas[len(lineas)-1].split("\t")
			primero=open(nombre_directorio+"\\"+str(contador+1)+"\\hist_test_"+ciclo+".txt","r")
			lineasPrimero = primero.readlines()
			primero.close()
			grado,cantidad = lineasPrimero[len(lineasPrimero)-1].split("\t")
			GRADOS.append(float(grado))
		gradoMedio=0
		for i in GRADOS:
			gradoMedio+=i
		gradoMedio/=len(GRADOS)
		if "anillo" in nombre_directorio:
			datosPromedio=open("semi-cooperadores.csv","a")
			resultados=[str(round(gradoMedio,4))]
			for j in anillo:
				if gradoMedio/j>=3:
					resultados.append("SI")
				else:
					resultados.append("NO")
			datosPromedio.write(nombre_directorio.replace("C:\\Users\\VG\\Documents\\Formación","")+","+resultados[0]+","+resultados[1]+","+resultados[2]+","+resultados[3]+"\n")
			datosPromedio.close()
		else:
			datosPromedio=open("semi-cooperadores.csv","a")
			resultados=[str(round(gradoMedio,4))]
			for j in malla:
				if gradoMedio/j>=3:
					resultados.append("SI")
				else:
					resultados.append("NO")
			datosPromedio.write(nombre_directorio.replace("C:\\Users\\VG\\Documents\\Formación","")+","+resultados[0]+","+resultados[1]+","+resultados[2]+","+resultados[3]+"\n")
			datosPromedio.close()