"""
Simulador de reconexión distribuida en redes complejas.

Se corre una simulación con
    python -m simulador.ejecutar parametros.json [carpeta]
o desde Python con simulador.ejecutar.simular(parametros, carpeta).

No lee configuracion.py ni hace análisis: solo registra la red de cada ciclo
y los mensajes (ver salida.py). El análisis está en la carpeta analisis/.
"""
