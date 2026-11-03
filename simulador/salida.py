"""
Archivos que escribe una corrida del simulador.

El simulador solo registra datos crudos; todas las medidas se calculan fuera,
en el análisis. Archivos de la carpeta de una corrida:

    parametros.json   parámetros de la corrida (lo escribe formacion.py)
    graph.adjlist     red base (ciclo 0)
    nodos.csv         nodo,x,y   coordenadas de cada nodo en la geometría de la red
    enlaces.csv       ciclo,nodo,enlace,conectado
                      estado de los enlaces dinámicos al terminar cada ciclo: el
                      enlace número `enlace` del nodo `nodo` está conectado con
                      `conectado` (los enlaces libres no aparecen). La red del
                      ciclo c es la red base más los enlaces del ciclo c.
    mensajes.csv      ciclo,tipo,mensajes   mensajes procesados en cada ciclo, por tipo
    resumen.json      ciclos completados, motivo de fin ("ciclos" o "diametro_2"),
                      ciclo en que el diámetro llegó a 2, mensajes totales,
                      tiempo de ejecución y semilla
"""

import csv
import json
from pathlib import Path


class Registro:
    """Escribe los archivos de una corrida mientras corre la simulación."""

    def __init__(self, carpeta):
        self.carpeta = Path(carpeta)
        self.carpeta.mkdir(parents=True, exist_ok=True)
        self._f_enlaces = open(self.carpeta / "enlaces.csv", "w", newline="", encoding="utf-8")
        self._f_mensajes = open(self.carpeta / "mensajes.csv", "w", newline="", encoding="utf-8")
        self._enlaces = csv.writer(self._f_enlaces)
        self._mensajes = csv.writer(self._f_mensajes)
        self._enlaces.writerow(["ciclo", "nodo", "enlace", "conectado"])
        self._mensajes.writerow(["ciclo", "tipo", "mensajes"])
        self._conteo_anterior = {}

    def nodos(self, red, ids):
        """Escribe las coordenadas de los nodos."""
        with open(self.carpeta / "nodos.csv", "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["nodo", "x", "y"])
            for i in ids:
                x, y = red.coordenadas(i)
                w.writerow([i, repr(float(x)), repr(float(y))])

    def ciclo(self, ciclo, modelos, conteos):
        """Registra el estado de los enlaces dinámicos y los mensajes de un ciclo.
        `modelos` es un diccionario id -> ComplexNetwork; `conteos` son los
        mensajes acumulados por tipo desde el inicio de la simulación."""
        for i in sorted(modelos):
            for enlace in modelos[i].enlacesDinamicos:
                if enlace.idConectado != -1:
                    self._enlaces.writerow([ciclo, i, enlace.idEnlace, enlace.idConectado])
        for tipo in conteos:
            delta = conteos[tipo] - self._conteo_anterior.get(tipo, 0)
            if delta:
                self._mensajes.writerow([ciclo, tipo, delta])
        self._conteo_anterior = dict(conteos)

    def cerrar(self, resumen):
        self._f_enlaces.close()
        self._f_mensajes.close()
        with open(self.carpeta / "resumen.json", "w", encoding="utf-8") as f:
            json.dump(resumen, f, ensure_ascii=False, indent=2)
            f.write("\n")
