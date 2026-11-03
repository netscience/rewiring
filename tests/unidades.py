"""Pruebas unitarias de las piezas del simulador que no dependen del motor de eventos:
redes.py (topologías y geometría), encaminamiento.py (ruteos) y reglas.py (selección
de candidatos).

Uso (desde la raíz del repositorio):
    python tests/unidades.py        # o: python -m unittest tests/unidades.py -v

Usa solo la biblioteca estándar (unittest), networkx y numpy.
"""

import math
import random
import sys
import types
import unittest
from collections import Counter
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))

import networkx as nx
import numpy as np

import redes
from encaminamiento import Encaminamiento
from reglas import Reglas


def cfg(**kw):
    """Configuración mínima con los atributos que leen las redes."""
    base = dict(ROWS=3, COLUMNS=4, NODOS_ANILLO=8)
    base.update(kw)
    return types.SimpleNamespace(**base)


def main_falso(red, nodos):
    """Sustituto del objeto Main con lo que usa Encaminamiento."""
    return types.SimpleNamespace(red=red, nodosTotales=nodos)


# ---------------------------------------------------------------------------
# redes.py
# ---------------------------------------------------------------------------

class PruebaMalla(unittest.TestCase):

    def setUp(self):
        self.red = redes.obtener_red("malla", cfg(ROWS=3, COLUMNS=4))
        self.G = self.red.construir()

    def test_nodos_y_aristas(self):
        self.assertEqual(sorted(self.G.nodes()), list(range(1, 13)))
        self.assertEqual(self.G.number_of_edges(), 3 * 3 + 2 * 4)  # 17

    def test_nombre(self):
        self.assertEqual(self.red.nombre(), "malla3x4")

    def test_coordenadas_por_filas(self):
        # Los nodos se numeran por filas: id = fila * COLUMNS + columna + 1
        self.assertEqual(self.red.coordenadas(1), (0, 0))
        self.assertEqual(self.red.coordenadas(4), (3, 0))
        self.assertEqual(self.red.coordenadas(5), (0, 1))
        self.assertEqual(self.red.coordenadas(12), (3, 2))

    def test_coordenadas_coinciden_con_aristas(self):
        # Toda arista de la malla une nodos a distancia euclidiana 1
        for u, v in self.G.edges():
            self.assertAlmostEqual(self.red.distancia(u, v), 1.0)

    def test_distancia_y_longitud_maxima(self):
        self.assertAlmostEqual(self.red.distancia(1, 12), math.hypot(3, 2))
        self.assertAlmostEqual(self.red.longitud_maxima(), math.hypot(2, 3))

    def test_malla_no_cuadrada_sin_coordenadas_repetidas(self):
        red = redes.obtener_red("malla", cfg(ROWS=5, COLUMNS=7))
        coords = [red.coordenadas(i) for i in range(1, 36)]
        self.assertEqual(len(set(coords)), 35)


class PruebaAnillo(unittest.TestCase):

    def setUp(self):
        self.red = redes.obtener_red("anillo", cfg(NODOS_ANILLO=8))
        self.G = self.red.construir()

    def test_nodos_y_aristas(self):
        self.assertEqual(sorted(self.G.nodes()), list(range(1, 9)))
        self.assertEqual(self.G.number_of_edges(), 8)
        self.assertTrue(all(d == 2 for _, d in self.G.degree()))

    def test_nombre(self):
        self.assertEqual(self.red.nombre(), "anillo8")

    def test_coordenadas_en_circulo_de_radio_10(self):
        for i in range(1, 9):
            x, y = self.red.coordenadas(i)
            self.assertAlmostEqual(math.hypot(x, y), 10.0)
        x, y = self.red.coordenadas(2)  # 2 * 360/8 = 90 grados
        self.assertAlmostEqual(x, 0.0, places=9)
        self.assertAlmostEqual(y, 10.0)

    def test_distancia_y_longitud_maxima(self):
        self.assertAlmostEqual(self.red.distancia(1, 5), 20.0)  # opuestos
        self.assertEqual(self.red.longitud_maxima(), 20)


class PruebaRegistro(unittest.TestCase):

    def test_red_desconocida(self):
        with self.assertRaises(ValueError):
            redes.obtener_red("toro", cfg())


# ---------------------------------------------------------------------------
# encaminamiento.py
# ---------------------------------------------------------------------------

class PruebaEncaminamiento(unittest.TestCase):

    def setUp(self):
        random.seed(1)
        self.red = redes.obtener_red("malla", cfg(ROWS=6, COLUMNS=6))
        self.G = self.red.construir()
        self.main = main_falso(self.red, 36)
        self.enc = Encaminamiento()

    def test_compass_elige_el_vecino_en_direccion_al_destino(self):
        # Nodo 1 en (0,0), vecinos 2 en (1,0) y 7 en (0,1)
        self.assertEqual(self.enc.Compass_Routing(1, [2, 7], 3, self.main), 2)   # destino (2,0)
        self.assertEqual(self.enc.Compass_Routing(1, [2, 7], 13, self.main), 7)  # destino (0,2)

    def test_compass_va_directo_si_el_destino_es_vecino(self):
        self.assertEqual(self.enc.Compass_Routing(1, [2, 7], 7, self.main), 7)

    def test_distancia_delegada_a_la_red(self):
        self.assertAlmostEqual(self.enc.distancia(1, 36, self.main), self.red.distancia(1, 36))

    def test_caminata_aleatoria_solo_elige_vecinos(self):
        vecinos = [2, 7]
        for _ in range(200):
            self.assertIn(self.enc.Random_Walk(1, vecinos), vecinos)

    def test_caminata_por_grado_proporcional_al_grado(self):
        G = nx.star_graph(4)  # centro 0 con grado 4, hojas con grado 1
        G.add_edge(5, 1)      # hoja 1 pasa a grado 2
        vecinos = [0, 1]      # grados 4 y 2: proporción 2:1
        c = Counter(self.enc.Random_Walk_Degree(9, vecinos, G) for _ in range(6000))
        self.assertAlmostEqual(c[0] / 6000, 2 / 3, delta=0.03)

    def test_caminata_por_grado_inverso(self):
        G = nx.star_graph(4)
        G.add_edge(5, 1)
        vecinos = [0, 1]      # pesos 1/4 y 1/2: proporción 1:2
        c = Counter(self.enc.Random_Walk_Inverse(9, vecinos, G) for _ in range(6000))
        self.assertAlmostEqual(c[0] / 6000, 1 / 3, delta=0.03)

    def test_node2vec_pesos(self):
        # Camino 0-1-2 y 1-3, con 0-3 unidos: desde 1 con prev = 0,
        # 0 es el anterior (1/p), 3 es vecino del anterior (1) y 2 no (1/q)
        G = nx.Graph([(0, 1), (1, 2), (1, 3), (0, 3)])
        p, q = 0.5, 2.0       # pesos: 0 -> 2, 3 -> 1, 2 -> 0.5
        c = Counter(self.enc.Random_Walk_Node2Vec(1, [0, 2, 3], G, prev=0, p=p, q=q) for _ in range(7000))
        self.assertAlmostEqual(c[0] / 7000, 2 / 3.5, delta=0.03)
        self.assertAlmostEqual(c[3] / 7000, 1 / 3.5, delta=0.03)
        self.assertAlmostEqual(c[2] / 7000, 0.5 / 3.5, delta=0.03)

    def test_node2vec_sin_anterior_elige_al_azar_entre_vecinos(self):
        G = nx.path_graph(3)
        for _ in range(100):
            self.assertIn(self.enc.Random_Walk_Node2Vec(1, [0, 2], G, prev=None), [0, 2])

    def test_destino_no_es_el_origen_ni_un_vecino(self):
        for _ in range(500):
            d = self.enc.generaDestino(1, self.main, [2, 7])
            self.assertNotIn(d, (1, 2, 7))
            self.assertTrue(1 <= d <= 36)

    def test_ruta_mas_corta(self):
        ruta = self.enc.shortestPath(self.G, 1, 36)
        self.assertEqual(ruta[0], 1)
        self.assertEqual(ruta[-1], 36)
        self.assertEqual(len(ruta) - 1, 10)  # distancia Manhattan en 6x6
        self.enc.clearShortestPathCache()
        self.assertEqual(self.enc.shortestPath(self.G, 1, 36), ruta)


# ---------------------------------------------------------------------------
# reglas.py
# ---------------------------------------------------------------------------

class PruebaReglas(unittest.TestCase):

    def setUp(self):
        np.random.seed(3)
        self.f_n = {5: 2, 7: 5, 9: 1}

    def regla(self, r, f_n=None, alpha=0, vp=None, vd=None, rutas=None):
        return Reglas(r, dict(self.f_n if f_n is None else f_n), alpha, vp, vd, rutas or [])

    def test_r1_el_mas_frecuente(self):
        self.assertEqual(self.regla(1).seleccionar_candidato(), 7)

    def test_r2_el_primero_descubierto(self):
        self.assertEqual(self.regla(2).seleccionar_candidato(), 5)

    def test_r3_proporcional_a_la_frecuencia(self):
        c = Counter(self.regla(3).seleccionar_candidato() for _ in range(8000))
        self.assertAlmostEqual(c[7] / 8000, 5 / 8, delta=0.03)
        self.assertAlmostEqual(c[5] / 8000, 2 / 8, delta=0.03)
        self.assertAlmostEqual(c[9] / 8000, 1 / 8, delta=0.03)

    def test_r4_solo_distancia(self):
        # alpha = 0: solo la matriz de distancia; la columna 0 es siempre el nodo 5
        rutas = [[5, 6], [5, 7]]
        for _ in range(50):
            self.assertEqual(self.regla(4, alpha=0, vp=[0, 1], vd=[1, 0], rutas=rutas).seleccionar_candidato(), 5)

    def test_r4_solo_popularidad(self):
        # alpha = 1: rutas reordenadas por popularidad ([5, 6] y [5, 7]); la columna 1 da 6 o 7
        rutas = [[5, 6], [5, 7]]
        c = Counter(self.regla(4, alpha=1, vp=[0, 1], vd=[1, 0], rutas=rutas).seleccionar_candidato() for _ in range(2000))
        self.assertEqual(set(c), {6, 7})

    def test_r4_sin_rutas(self):
        self.assertEqual(self.regla(4, alpha=0.3, vp=[1, 1], vd=[1, 1], rutas=[]).seleccionar_candidato(), -1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
