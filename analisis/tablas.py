"""
Tablas Medidas_estructurales (formato anterior de 5creaTablasFormacion.py): una
por red, regla y exploración, con una columna por longitud de enlace, con el
agrupamiento, el ASPL y el diámetro promedio por ciclo y la distribución de
grados de la red final normalizada por el número de nodos.
"""

import os
from collections import OrderedDict
from pathlib import Path

from .lectura import Corrida, ejecuciones


def crea_tablas(resultados, configs):
    destino = Path(resultados) / "Medidas_estructurales"
    os.makedirs(destino, exist_ok=True)
    grupos = OrderedDict()
    for config in configs:
        if config.name.startswith("D") and config.name[1:].isdigit():
            grupos.setdefault(config.parent, []).append(config)
    for base, cfgs in grupos.items():
        cfgs.sort(key=lambda c: int(c.name[1:]))
        rel = base.relative_to(resultados).parts
        if len(rel) < 3:
            continue
        nombre_red, regla, routing = rel[-3:]
        nodos = Corrida(ejecuciones(cfgs[0])[0]).nodos
        CAP, LTP, DIAM, GRA = [], [], [], []
        for c in cfgs:
            lineas = (c / "datos-promedio.csv").read_text(encoding="utf-8").splitlines()[1:]
            partes = [l.split(",") for l in lineas]
            CAP.append([p[1] for p in partes])
            LTP.append([p[2] for p in partes])
            DIAM.append([p[3] for p in partes])
            lineas = (c / "datos-promedio_grados.csv").read_text(encoding="utf-8").splitlines()[1:]
            GRA.append([l.split(",")[1] for l in lineas])
        cols = "".join(c.name + "," for c in cfgs)
        with open(destino / f"Medidas_estructurales_{nombre_red}_{regla}_{routing}.csv", "w", encoding="utf-8") as f:
            for titulo, datos in ((",Coeficiente de Agrupamiento", CAP), ("\n\n,Longitud de Trayectoria Promedio", LTP),
                                  ("\n\n,Diámetro", DIAM)):
                f.write(titulo + "\n," + cols + "\n")
                for i in range(len(datos[0])):
                    f.write(str(i) + "," + "".join(s[i] + "," for s in datos) + "\n")
            f.write("\n\n,Distribución de Grados\n," + cols + "\n")
            for i in range(max(len(g) for g in GRA)):
                f.write(str(i) + ",")
                for g in GRA:
                    f.write(str(float(g[i]) / nodos) + "," if i < len(g) else ",")
                f.write("\n")
