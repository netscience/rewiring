import numpy as np
import operator
from collections import Counter
import copy

class Reglas:
    def __init__(self,regla,vector_popularidad,vector_distancia,alpha,logFile,f_n,paquetes,rutas):
        self.r=regla
        self.vector_popularidad=vector_popularidad
        self.vector_distancia=vector_distancia
        self.alpha=alpha
        self.f_n=f_n 
        self.paquetes=paquetes
        self.log_file=logFile
        self.rutas=rutas
        self.candidato=-1
    
    def registrar_evento(self):
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write("\n--------------------------------------\n")
            f.write(f"Regla ejecutada: {self.r}\n")
            f.write(f"Vector popularidad: {self.vector_popularidad}\n")
            f.write(f"Vector distancia: {self.vector_distancia}\n")
            f.write(f"Alpha: {self.alpha}\n")
            f.write(f"f_n: {self.f_n}\n")
            f.write("Paquetes:\n")
            for p in self.paquetes:
                f.write(f"   - {getattr(p, 'rutaAuxiliar', 'sin rutaAuxiliar')}\n")
            for r in self.rutas:
                f.write(f"   - Ruta en matriz: {r}\n")
            f.write(f"Candidato seleccionado: {self.candidato}\n")
            
    def seleccionar_candidato(self):
        if self.r==1:
            self.candidato=self.regla_1()
        elif self.r==2:
            self.candidato=self.regla_2()
        elif self.r==3:
            self.candidato=self.regla_3()
        elif self.r==4:
            self.candidato=self.regla_4()
        self.registrar_evento()
        return self.candidato

    def regla_1(self):
        self.f_n = sorted(self.f_n.items(), key=operator.itemgetter(1), reverse=True)# Ordeno el diccionario f_n de mayor a menor frecuencia
        self.f_n = dict(self.f_n)#convierto la lista de tuplas en un diccionario nuevamente, pero ya ordenado
        claves=list(self.f_n.keys())#obtengo las claves del diccionario f_n, en este caso son los id´s de los nodos visitados
        clave=claves[0]
        return clave

    def regla_2(self):
        claves=list(self.f_n.keys())#obtengo las claves del diccionario f_n, en este caso son los id´s de los nodos visitados
        clave=claves[0]
        return clave
    
    def regla_3(self):
        llaves=list(self.f_n.keys())
        probabilidades=list(self.f_n.values())
        probabilidades=probabilidades/np.sum(probabilidades)
        clave=np.random.choice(llaves,p=probabilidades)
        return clave
    
    def frecuencia(self,matriz, vector):
        if len(matriz)==0:                                            # Matriz vacia
            return {} 
        filas = len(matriz)                                           # Número de filas
        columnas = len(vector)                                     # Número de columnas
        suma_seleccionados = 0                                        # Suma de nodos seleccionados
        indices_seleccionados = [i for i in range(columnas) if vector[i]!=0]  # Lista de indices seleccionados del vector
        long = len(indices_seleccionados)                             # Total de columnas seleccionadas
        seleccion = [[0 for i in range(long)] for i in range(filas)]  # Matriz de ceros para las columnas seleccionadas
        frecuencia = {}                                               # Diccionarios de frecuencias de cada nodo
        for i in range(filas):
            for posicion, indice in enumerate(indices_seleccionados):
                nodo = vector[indice]*matriz[i][indice]
            if nodo != 0:
                suma_seleccionados += 1                                 # Total de nodos seleccionados sin contar el cero
                seleccion[i][posicion] = nodo                           # Guarda los nodos seleccionados
                if nodo in frecuencia:                                  # Si ya se encuentra el nodo en el diccionario,
                    frecuencia[nodo] += 1                                 # entonces suma un uno
                else:
                    frecuencia[nodo] = 1                                  # Si no, colocar un uno
        if 0 in frecuencia:
            del frecuencia[0]
        return frecuencia
    
    def matrices(self,long):                   # Recibe una lista de listas
        distancia = []
        popularidad = []
        listas = copy.deepcopy(self.rutas)
        if len(listas)==0 or all(len(sublista) == 0 for sublista in listas):
                return popularidad, distancia
        listas = [j for j in listas if j]           # Si encuentro una lista vacia
        for posicion, lista in enumerate(listas):   # Obtenemos la matriz de distancia con listas de igual longitud
            if len(lista) > long:                     # Si la lista es mayor a longitud
                lista = lista[:long]                    # Cortar la lista hasta la longitud
                listas[posicion] = lista                # Reemplazar la lista recortada
        lista = [i for num in listas for i in num]  # Convertir la lista de listas en una sola lista.
        conteo = Counter(lista)                     # Diccionario con el conteo de cada nodo en la lista.
        for lista in listas:                        # Llenar la lista de distancia con listas de igual longitud
            if len(lista) == long:                    # Si la lista es igual a la longitud
                distancia.append(lista)                 # Agregar la lista directamente
            if len(lista) < long:                     # Si la lista es menor que longitud
                while len(lista) < long:
                    lista.append(0)                       # Rellenar de ceros la lista
                distancia.append(lista)
            reordenar_lista = sorted(lista, key=lambda x: conteo.get(x,0), reverse=True) # Ordena en función de la frecuencia, de mayor a menor
            popularidad.append(reordenar_lista)       # Reordenamos para obtener la matriz de popularidad
        return popularidad, distancia
    
    def nodos_seleccionados(self, popularidad, distancia):
        frecuencias_popularidad = self.frecuencia(popularidad, self.vector_popularidad)
        frecuencias_distancia = self.frecuencia(distancia, self.vector_distancia)
        claves = set(frecuencias_popularidad.keys()) | set(frecuencias_distancia.keys())
        if (len(frecuencias_distancia)==0 and self.alpha==0) or (len(frecuencias_popularidad)==0 and self.alpha==1) or (len(frecuencias_distancia)==0 and len(frecuencias_popularidad)==0): # Sin ambos diccionarios son vacios
            return {}   
        if self.alpha==0:
            return frecuencias_distancia                                                          
        elif self.alpha==1:                 
            return frecuencias_popularidad
        else: 
            claves = set(frecuencias_popularidad.keys()) | set(frecuencias_distancia.keys())    
            freq = {}
            for nodo in claves:
                frecuencia_popularidad = frecuencias_popularidad.get(nodo, 0)
                frecuencia_distancia = frecuencias_distancia.get(nodo, 0)
                freq[nodo] = self.alpha*frecuencia_popularidad + (1-self.alpha)*frecuencia_distancia # Modelo representativo de las reglas
            return freq
    
    def regla_4(self):
        long = len(self.vector_distancia)
        popularidad, distancia = self.matrices(long)
        probabilidad=self.nodos_seleccionados(popularidad, distancia)
        if len(probabilidad)==0:
            return -1
        probabilidades = np.array(list(probabilidad.values()), dtype=float)
        suma = np.sum(probabilidades)
        probabilidades = probabilidades/suma
        probabilidad_normalizada = dict(zip(probabilidad.keys(), probabilidades))
        #Elegir un nodo candidato
        nodos = list(probabilidad_normalizada.keys())
        proba = list(probabilidad_normalizada.values())
        candidato = np.random.choice(nodos, p=proba)
        return candidato