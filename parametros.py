"""
Parámetros de una corrida del simulador.

Una corrida queda descrita por completo por un objeto `Parametros`, que se
guarda como parametros.json en la carpeta de la corrida. ejecutar.py lee ese
archivo y corre la simulación; formacion.py lo escribe para cada corrida de una
serie de experimentos. Así el simulador no depende de configuracion.py ni de
un config.py copiado en cada carpeta de resultados.

Ejemplo de parametros.json:

    {
      "red": "malla",
      "geometria": {"ROWS": 8, "COLUMNS": 8},
      "routing": "RANDOM-WALK",
      "regla": 1,
      "long_enlace": 1,
      "ciclos": 2,
      "enlaces_dinamicos": 2,
      "exploradores": 4,
      "div_conexiones": 1,
      "p": 0, "q": 0,
      "alpha": 0, "vector_popularidad": 0, "vector_distancia": 0,
      "semilla": 123456
    }
"""

import json
from dataclasses import asdict, dataclass, field, fields
from pathlib import Path
from types import SimpleNamespace


@dataclass
class Parametros:
    red: str                    # Clave de la red en redes.py: "malla", "anillo", ...
    geometria: dict             # Parámetros de la red, p.e. {"ROWS": 8, "COLUMNS": 8}
    routing: str                # Exploración: "RANDOM-WALK", "COMPASS-ROUTING", "SHORTEST-PATH", "RW-DEGREE", "RW-INVERSE", "RW-NODE2VEC"
    regla: int                  # Regla de reconexión: 1, 2, 3, 4
    long_enlace: int            # Divisor de la longitud máxima de los enlaces dinámicos
    ciclos: int                 # Número de ciclos de reconexión
    enlaces_dinamicos: int      # Número de enlaces dinámicos por nodo
    exploradores: int           # Número de paquetes exploradores por ciclo
    div_conexiones: int = 1     # Máximo de conexiones por nodo = num_nodos / div_conexiones
    p: float = 0                # Parámetros de Node2Vec (solo RW-NODE2VEC)
    q: float = 0
    alpha: float = 0            # Parámetros de R4 (solo regla 4)
    vector_popularidad: object = 0
    vector_distancia: object = 0
    semilla: object = None      # Entero, o None para una corrida no reproducible
    extra: dict = field(default_factory=dict)  # Parámetros adicionales de nuevas reglas o redes

    #---Geometría para redes.py---

    def cfg_red(self):
        """Objeto con la geometría como atributos, como lo espera redes.obtener_red."""
        return SimpleNamespace(**self.geometria)

    #---Lectura y escritura---

    def a_dict(self):
        return asdict(self)

    def guardar(self, ruta):
        """Escribe los parámetros en un archivo JSON."""
        Path(ruta).write_text(json.dumps(self.a_dict(), ensure_ascii=False, indent=2) + "\n",
                              encoding="utf-8")

    @classmethod
    def desde_dict(cls, datos):
        conocidos = {f.name for f in fields(cls)}
        desconocidos = set(datos) - conocidos
        if desconocidos:
            raise ValueError(f"Parámetros desconocidos: {sorted(desconocidos)}")
        return cls(**datos)

    @classmethod
    def leer(cls, ruta):
        """Lee los parámetros de un archivo JSON."""
        return cls.desde_dict(json.loads(Path(ruta).read_text(encoding="utf-8")))

    @classmethod
    def desde_config(cls, config, semilla=None):
        """Construye los parámetros a partir de un módulo config.py con constantes
        en mayúsculas (el formato anterior). Se conserva para main.py y las pruebas."""
        import redes
        red = config.RED
        clase = redes.REDES.get(red)
        nombres = clase.PARAMETROS if clase is not None else ()
        return cls(
            red=red,
            geometria={n: getattr(config, n) for n in nombres},
            routing=config.ROUTING,
            regla=config.REGLA,
            long_enlace=config.LONG_ENLACE,
            ciclos=config.CICLOS,
            enlaces_dinamicos=config.ENLACES_DINAMICOS,
            exploradores=config.EXPLORADORES,
            div_conexiones=config.DIV_CONEXIONES,
            p=getattr(config, "P", 0),
            q=getattr(config, "Q", 0),
            alpha=getattr(config, "ALPHA", 0),
            vector_popularidad=getattr(config, "VECTOR_POPULARIDAD", 0),
            vector_distancia=getattr(config, "VECTOR_DISTANCIA", 0),
            semilla=semilla if semilla is not None else getattr(config, "SEMILLA", None),
        )
