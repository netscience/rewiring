
import os

ejemplo_dir = 'C:\\Users\\VG\\Documents\\Formación'#este es el directorio que recorrere recursivamente

for nombre_directorio, directorios, ficheros in os.walk(ejemplo_dir):#recorro recursivamente un directorio
	CANTIDADES=[]
	if ("1" in directorios and "2" in directorios and "3" in directorios):
		for contador,direc in enumerate(directorios):
			archivo=open(nombre_directorio+"\\"+str(contador+1)+"\\datos-salida_"+str(contador+1)+".txt","r")
			lineas=archivo.readlines()
			archivo.close()
			ciclo,AVCL,components,diam,APL,order = lineas[len(lineas)-1].split("\t")
			primero=open(nombre_directorio+"\\"+str(contador+1)+"\\hist_test_"+ciclo+".txt","r")
			lineasPrimero = primero.readlines()
			primero.close()
			CANTIDAD_1=[]
			for linea in lineasPrimero:
				grado,cantidad = linea.split("\t")
				CANTIDAD_1.append(cantidad)
			CANTIDADES.append(CANTIDAD_1)
		maximo=-1000
		for i in CANTIDADES:
			if len(i)>maximo:
				maximo=len(i)
		CANTIDADES_PROMEDIO=[]
		for i in range(maximo):
			valor=0
			for j in range(len(CANTIDADES)):
				try:
					primero=CANTIDADES[j][i]
				except IndexError as error:
					primero=0
				valor+=float(primero)
			valor/=len(CANTIDADES)
			CANTIDADES_PROMEDIO.append(valor)
		datosPromedio=open(nombre_directorio+"\\datos-promedio_grados.csv","w")
		for i in range(maximo):
			datosPromedio.write('{0:.6f}\n'.format(CANTIDADES_PROMEDIO[i]))
		datosPromedio.close()
	"""for nombre_subdirectorio in directorios:
		print("subdirectorio",nombre_subdirectorio)
	for nombre_fichero in ficheros:
		print("archivo",nombre_fichero)"""