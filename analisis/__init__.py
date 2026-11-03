"""
Análisis de los resultados del simulador.

Lee solo la carpeta de resultados (no importa el simulador): en cada corrida,
parametros.json, la red base (graph.adjlist), las coordenadas (nodos.csv), la
red de cada ciclo (enlaces.csv) y los mensajes (mensajes.csv). También lee
resultados del formato anterior (salida_<n>.txt y config.py).

Uso:
    python analisis/analizar.py [carpeta_resultados]
"""
