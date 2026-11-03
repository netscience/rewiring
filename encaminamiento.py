
import random
import math
import networkx as nx

# Ángulos (en grados) que difieren en menos de esto se consideran iguales en Compass Routing
TOLERANCIA_ANGULO = 1e-9

class Encaminamiento:

    def __init__(self):
        self._sp_cache = {}           # {source: {dest: path}}

    #---DISTANCIA---------------------------------

    def distancia(self,node1,node2,main):
        """Distancia euclidiana entre dos nodos, según la geometría de la red (ver redes.py)"""
        return main.red.distancia(node1,node2)

    #---COMPASS ROUTING--------------------------

    def angulo(self,destino,origen,nodo,main):
        #print("or",origen,"des",destino,"vecino",nodo)
        p0 = main.red.coordenadas(origen)
        p1 = main.red.coordenadas(destino)
        p2 = main.red.coordenadas(nodo)
        #print("origen",p0)
        #print("destino",p1)
        #print("vecino",p2)
        u1 = p1[0]-p0[0]
        #print("u1",u1)
        u2 = p1[1]-p0[1]
        #print("u2",u2)
        v1 = p2[0]-p0[0]
        #print("v1",v1)
        v2 = p2[1]-p0[1]
        #print("v2",v2)
        #calculo del angulo entre vectores mediante producto punto
        div = (u1*v1+u2*v2)/((math.sqrt((math.pow(u1,2) + math.pow(u2,2))))*(math.sqrt((math.pow(v1,2) + math.pow(v2,2)))))
        try:
            angC=math.degrees(math.acos(div))
        except ValueError as error:
            if div>1.0:
                #print("mas grande",div)
                div=1.0
            elif div < -1.0:
                #print("mas pequeño",div)
                div=-1.0
            angC=math.degrees(math.acos(div))
        #print("angC",angC)
        return angC

    def Compass_Routing(self,identificador,vecinos,destino,main):
        """Reenvía al vecino que forma el menor ángulo con la dirección al destino.

        Empates: si varios vecinos forman el menor ángulo, gana el último de la
        lista (la regla de siempre). Dos ángulos que difieren en menos de
        TOLERANCIA_ANGULO grados se consideran iguales: en el anillo, por ejemplo,
        con el destino diametralmente opuesto ambos vecinos forman el mismo ángulo,
        pero el redondeo de senos y cosenos los hace diferir en el decimal 14, y
        esa diferencia cambia entre sistemas operativos."""
        w = random.choice(vecinos)
        #print("origen",identificador,"destino",destino,"vecinos",vecinos)
        if destino in vecinos:
            w = destino
        else:
            angulos = [self.angulo(destino,identificador,vecino,main) for vecino in vecinos]
            minimo = min(angulos)
            for vecino, ang2 in zip(vecinos, angulos):
                if ang2 <= minimo + TOLERANCIA_ANGULO:
                    w = vecino
        #print("vecino seleccionado",w)
        return w 

    #---SHORTEST PATH (DIJKSTRA)----------------

    def shortestPath(self,grafo,fuente,destino):
        if fuente not in self._sp_cache:
            self._sp_cache[fuente] = dict(nx.single_source_shortest_path(grafo, fuente))
        return list(self._sp_cache[fuente][destino])

    def clearShortestPathCache(self):
        """Limpia la caché de rutas más cortas (necesario entre ciclos cuando la topología cambia)."""
        self._sp_cache.clear()

    #---RANDOM WALK-----------------------------

    def Random_Walk(self,identificador,vecinos):
        w=random.choice(vecinos)
        return w

    def Random_Walk_Degree(self,identificador,vecinos,grafo):
        """Caminata sesgada por grado.
        P(u) = deg(u) / sum(deg(v) for v in vecinos)
        Favorece saltar hacia nodos de mayor conectividad (hubs).
        """
        pesos = [grafo.degree(u) for u in vecinos]
        total = sum(pesos)
        if total == 0:
            return random.choice(vecinos)
        return random.choices(vecinos, weights=pesos, k=1)[0]

    def Random_Walk_Inverse(self,identificador,vecinos,grafo):
        """Caminata sesgada por grado inverso.
        P(u) = (1/deg(u)) / sum(1/deg(v) for v in vecinos)
        Favorece saltar hacia nodos de menor conectividad (periféricos).
        """
        pesos = [1.0 / grafo.degree(u) for u in vecinos]
        total = sum(pesos)
        if total == 0:
            return random.choice(vecinos)
        return random.choices(vecinos, weights=pesos, k=1)[0]

    def Random_Walk_Node2Vec(self,identificador,vecinos,grafo,prev=None,p=1.0,q=1.0):
        """Caminata node2vec.
        Los parámetros p y q controlan el sesgo de retorno y de exploración:
            alpha(x) = 1/p  si x == prev          (retorno al nodo anterior)
                     = 1    si x es vecino de prev  (triángulo local / BFS)
                     = 1/q  en otro caso            (exploración DFS)
        p > 1 desincentiva volver atrás.
        q < 1 favorece exploración hacia nodos lejanos (DFS).
        q > 1 favorece exploración local (BFS).
        """
        if prev is None:
            return random.choice(vecinos)
        vecinos_prev = set(grafo.neighbors(prev))
        pesos = []
        for x in vecinos:
            if x == prev:
                alpha = 1.0 / p
            elif x in vecinos_prev:
                alpha = 1.0
            else:
                alpha = 1.0 / q
            pesos.append(alpha)
        return random.choices(vecinos, weights=pesos, k=1)[0]

    #---EXTRAS----------------------------------

    def generaDestino(self,identificador,main,vecinos):
        """genera un nodo destino de manera aleatoria (que no esté en mis vecinos)"""
        d = False
        while(d == False):
            dest = random.randint(1,main.nodosTotales)
            if dest != identificador and dest not in vecinos:
                d = True
        return dest