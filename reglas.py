import numpy as np
import operator


class Reglas:
    def __init__(self,regla,logFile,f_n,paquetes,rutas):
        self.r=regla
        self.f_n=f_n 
        self.paquetes=paquetes
        self.log_file=logFile
        self.rutas=rutas
        self.candidato=None
    
    def registrar_evento(self):
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write("\n--------------------------------------\n")
            f.write(f"Regla ejecutada: {self.r}\n")
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
        #print("soy",self.id,"ejecuto R3 mis llaves son:",llaves)
        #print("soy",self.id,"ejecuto R3 mis probabilidades son:",list(probabilidades))
        clave=np.random.choice(llaves,p=probabilidades)
        #print("soy",self.id,"selecciono a",clave,"con f_n",self.f_n[clave])
        return clave