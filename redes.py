"""
Creación de las redes (topologías iniciales) sobre las que se desarrolla la simulación.

Cada tipo de red es una subclase de `Red` registrada en el diccionario `REDES`.
Además de construir el grafo, cada red define la geometría de sus nodos
(coordenadas y distancia), que usan Compass Routing y la restricción de
longitud de los enlaces dinámicos.

Las clases reciben un módulo de configuración (`configuracion` desde los scripts
de experimentos o `config` desde main.py), por lo que no dependen de ninguno.

Para agregar un nuevo tipo de red:
  1. Crear una subclase de `Red` definiendo CLAVE, nombre(), construir(),
     longitud_maxima() y _calcular_coordenadas().
  2. Registrarla en `REDES` (al final de este archivo).
  3. Agregar sus parámetros en configuracion.py y escribirlos en config.py
     desde formacion.py (generar_script_constantes).
"""

import math
import networkx as nx


class Red:
    """Clase base para todos los tipos de red."""

    CLAVE = None   # Identificador de la red: se usa en configuracion.RED y config.RED (p.e. "malla")

    def __init__(self, cfg):
        self.cfg = cfg
        self._coordenadas = {}  # Caché de coordenadas {nodeId: (x, y)}

    #---Métodos que debe implementar cada red---

    def nombre(self):
        """Nombre de la red usado en el directorio de resultados."""
        raise NotImplementedError

    def construir(self):
        """Regresa un grafo NetworkX con nodos etiquetados de 1 a N."""
        raise NotImplementedError

    def longitud_maxima(self):
        """Longitud máxima de un enlace dinámico (antes de dividir entre LONG_ENLACE)."""
        raise NotImplementedError

    def _calcular_coordenadas(self, nodeId):
        """Regresa las coordenadas (x, y) del nodo en el plano."""
        raise NotImplementedError

    #---Métodos comunes---

    def coordenadas(self, nodeId):
        """Coordenadas (x, y) del nodo (con caché)."""
        if nodeId not in self._coordenadas:
            self._coordenadas[nodeId] = self._calcular_coordenadas(nodeId)
        return self._coordenadas[nodeId]

    def distancia(self, node1, node2):
        """Distancia euclidiana entre dos nodos."""
        n1 = self.coordenadas(node1)
        n2 = self.coordenadas(node2)
        return math.sqrt(math.pow(n2[0] - n1[0], 2) + math.pow(n2[1] - n1[1], 2))

    @staticmethod
    def _etiquetar(grafo):
        """Etiqueta los nodos con enteros a partir de 1, en orden."""
        return nx.convert_node_labels_to_integers(grafo, first_label=1, ordering="sorted")


#---MALLA----------------------------

class Malla(Red):
    CLAVE = "malla"

    def nombre(self):
        return f"malla{self.cfg.ROWS}x{self.cfg.COLUMNS}"

    def construir(self):
        grafo = nx.grid_2d_graph(self.cfg.ROWS, self.cfg.COLUMNS, periodic=False)
        return self._etiquetar(grafo)

    def longitud_maxima(self):
        # Longitud de la diagonal principal de la malla
        n1 = [0, 0]
        n2 = [self.cfg.ROWS - 1, self.cfg.COLUMNS - 1]
        return math.sqrt(math.pow(n2[0] - n1[0], 2) + math.pow(n2[1] - n1[1], 2))

    def _calcular_coordenadas(self, nodeId):
        x = (nodeId - 1) % self.cfg.COLUMNS
        y = (nodeId - 1) // self.cfg.COLUMNS
        return (x, y)


#---ANILLO----------------------------

class Anillo(Red):
    CLAVE = "anillo"
    RADIO = 10               # Radio del anillo en unidades
    DIAMETRO = 2 * RADIO

    def nombre(self):
        return f"anillo{self.cfg.NODOS_ANILLO}"

    def construir(self):
        grafo = nx.circulant_graph(self.cfg.NODOS_ANILLO, [1])
        return self._etiquetar(grafo)

    def longitud_maxima(self):
        return self.DIAMETRO

    def _calcular_coordenadas(self, nodeId):
        #transformación de coordenadas polares a rectangulares:
        angulo = math.radians((360 / self.cfg.NODOS_ANILLO) * nodeId)
        x = self.RADIO * math.cos(angulo)
        y = self.RADIO * math.sin(angulo)
        return (x, y)


#---REGISTRO DE REDES------------------

# Agregar aquí las nuevas redes
REDES = {cls.CLAVE: cls for cls in (Malla, Anillo)}


def obtener_red(clave, cfg):
    """Regresa una instancia de la red indicada por su clave (p.e. "malla").

    Lanza ValueError si el tipo de red no existe.
    """
    cls = REDES.get(clave)
    if cls is None:
        raise ValueError(f"Tipo de red desconocido: {clave}. Disponibles: {list(REDES)}")
    return cls(cfg)
