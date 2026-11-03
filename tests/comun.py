"""Funciones compartidas por las pruebas de extremo a extremo."""

import json
import os
import re

IGNORAR = re.compile(r"(\.pyc$|__pycache__)")


def normaliza(ruta, texto):
    """Quita lo que cambia entre máquinas o días sin cambiar los resultados."""
    if ruta.endswith(".adjlist"):
        # networkx escribe comentarios con la línea de comandos y la fecha
        return "\n".join(l for l in texto.splitlines() if not l.startswith("#")) + "\n"
    if ruta.endswith(".gexf"):
        texto = re.sub(r'lastmodifieddate="[^"]*"', 'lastmodifieddate=""', texto)
        texto = re.sub(r"<creator>.*?</creator>", "<creator/>", texto)
    if ruta.endswith("resumen.json"):
        datos = json.loads(texto)
        datos.pop("tiempo_s", None)
        return json.dumps(datos, sort_keys=True)
    return texto


def recoge(resultados, omitir=()):
    """Diccionario ruta relativa -> contenido normalizado (o marca de existencia para PNG)."""
    salida = {}
    for raiz, dirs, archivos in os.walk(resultados):
        dirs[:] = [d for d in dirs if d != "__pycache__"]
        for nombre in archivos:
            completa = os.path.join(raiz, nombre)
            rel = os.path.relpath(completa, resultados)
            if IGNORAR.search(rel) or rel in omitir:
                continue
            if nombre.endswith(".png"):
                salida[rel] = "<png>"
            else:
                with open(completa, encoding="utf-8", errors="replace") as f:
                    salida[rel] = normaliza(rel, f.read())
    return dict(sorted(salida.items()))


def compara(esperado, obtenido):
    """Imprime las diferencias y regresa True si todo coincide."""
    faltan = sorted(set(esperado) - set(obtenido))
    sobran = sorted(set(obtenido) - set(esperado))
    distintos = sorted(k for k in set(esperado) & set(obtenido) if esperado[k] != obtenido[k])
    for titulo, lista in (("Faltan", faltan), ("Sobran", sobran), ("Distintos", distintos)):
        if lista:
            print(f"{titulo} ({len(lista)}):")
            for k in lista[:15]:
                print(f"    {k}")
            if len(lista) > 15:
                print(f"    ... y {len(lista) - 15} más")
    iguales = len(set(esperado) & set(obtenido)) - len(distintos)
    print(f"\n{iguales} de {len(esperado)} archivos coinciden con la referencia")
    return not (faltan or sobran or distintos)
