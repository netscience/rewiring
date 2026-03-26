# Rewiring: Simulador de Reconexión en Redes Complejas

## Descripción General

Simulador de eventos discretos para **modelos de reconexión distribuida en redes complejas**, desarrollado en el marco del proyecto de Ciencia de Frontera **CBF-2025-G-1812** (SECIHTI). Se implementa en Python usando NetworkX como base para la creación y análisis de gráficas.

---

## Arquitectura

```mermaid
graph TD
    subgraph "Motor de Simulación"
        SIM["Simulator<br/>Motor de eventos"]
        SIMUL["Simulation<br/>Orquestador"]
        PROC["Process<br/>Entidad activa por nodo"]
        MODEL["Model<br/>Clase abstracta"]
        EVT["Event<br/>Mensaje entre procesos"]
    end

    subgraph "Modelo de Dominio"
        CN["ComplexNetwork<br/>Algoritmo de reconexión<br/>(621 líneas)"]
        PKG["Paquete<br/>Paquete explorador"]
        ENC["Encaminamiento<br/>Algoritmos de ruteo"]
        ENL["Enlace<br/>Enlace dinámico"]
        REG["Reglas<br/>Reglas de recableado"]
    end

    subgraph "Configuración"
        CONF["configuracion.py<br/>Parámetros del experimento"]
        CONFV["configVisualizacion.py<br/>Parámetros de visualización"]
    end

    subgraph "Pipeline de Ejecución (numerado)"
        S0["0creaCopiaSimulador.py<br/>Crea árbol de directorios"]
        FORM["formacion.py<br/>Ejecuta series de experimentos"]
        S1["1creaPromediosFormacion.py<br/>Promedios AvCl, ASPL, Diámetro"]
        S2["2creaPromediosDistGradosFormacion.py<br/>Promedios dist. grados"]
        S3["3creaImagenesPNG.py<br/>Visualización de grafos"]
        S4["4creaGEXF.py<br/>Exporta grafos a GEXF"]
        S5["5creaTablasFormacion.py<br/>Tablas CSV finales"]
    end

    MAIN["main.py<br/>Punto de entrada"] --> SIMUL
    SIMUL --> SIM
    SIMUL --> PROC
    PROC --> MODEL
    MODEL --> CN
    CN --> PKG
    CN --> ENC
    CN --> ENL
    CN --> REG
    EVT -.-> SIM

    CONF --> MAIN
    CONF --> S0
    CONF --> FORM
    FORM --> MAIN
    S0 --> FORM
    FORM -.-> S1
    S1 -.-> S2
    S2 -.-> S3
    S3 -.-> S4
    S4 -.-> S5
```

---

## Componentes Principales

### Motor de Simulación de Eventos Discretos

| Archivo | Líneas | Responsabilidad |
|---------|--------|-----------------|
| [simulator.py](file:///Users/usuario/Repositorios/rewiring/simulator.py) | 47 | Motor con agenda ordenada por tiempo. Inserta/extrae eventos en orden causal |
| [simulation.py](file:///Users/usuario/Repositorios/rewiring/simulation.py) | 79 | Orquesta el experimento: lee el grafo, crea procesos, ejecuta el bucle principal |
| [process.py](file:///Users/usuario/Repositorios/rewiring/process.py) | 80 | Entidad activa en cada nodo. Asocia modelos y reenvía eventos |
| [model.py](file:///Users/usuario/Repositorios/rewiring/model.py) | 83 | Clase abstracta base con métodos [init()](file:///Users/usuario/Repositorios/rewiring/simulation.py#65-68), [receive()](file:///Users/usuario/Repositorios/rewiring/process.py#53-57), [send()](file:///Users/usuario/Repositorios/rewiring/model.py#80-84) |
| [event.py](file:///Users/usuario/Repositorios/rewiring/event.py) | 54 | Encapsula: nombre, tiempo, destino, fuente, paquete, puerto |

### Modelo de Reconexión Distribuida

| Archivo | Líneas | Responsabilidad |
|---------|--------|-----------------|
| [complexNetwork.py](file:///Users/usuario/Repositorios/rewiring/complexNetwork.py) | 621 | **Núcleo del simulador**. Implementa las 3 fases del ciclo de reconexión |
| [paquete.py](file:///Users/usuario/Repositorios/rewiring/paquete.py) | 73 | Paquete explorador: lleva ruta, destino, distancia máxima, ID de enlace |
| [encaminamiento.py](file:///Users/usuario/Repositorios/rewiring/encaminamiento.py) | 119 | 3 algoritmos de ruteo + cálculo de distancias en malla y anillo |
| [enlace.py](file:///Users/usuario/Repositorios/rewiring/enlace.py) | 40 | Enlace dinámico: ID, longitud máxima, estado libre/ocupado, nodo conectado |
| [reglas.py](file:///Users/usuario/Repositorios/rewiring/reglas.py) | 56 | 3 reglas de selección de candidato a reconexión |

---

## Algoritmo de Reconexión (3 Fases por Ciclo)

Cada ciclo de simulación ejecuta 3 fases coordinadas mediante **PIF (Propagation of Information with Feedback)**:

### Fase 1: Exploración (`PIF-EXPLORACION`)
- Cada nodo envía `N` **paquetes exploradores** a la red
- Los paquetes viajan usando uno de los 3 algoritmos de ruteo
- Al regresar (vía `ACK`), se actualizan:
  - `f_n`: frecuencia de visita a nodos no-vecinos
  - `f_e`: frecuencia de uso de enlaces dinámicos

### Fase 2: Negociación (`PIF-NEGOCIACION`)
- Cada nodo selecciona candidatos a conexión usando `f_n` y una regla
- Si tiene enlaces libres → envía `SOLICITUD-CONEXION`
- Si no tiene enlaces libres → evalúa recableado del enlace menos usado (`f_e`)
- Los destinos responden con `ACEPTO-CONEXION` o `RECHAZO-CONEXION`
- Se desempatan solicitudes cruzadas (gana el ID mayor)

### Fase 3: Conexión (`PIF-CONEXION`)
- Se materializan las conexiones/desconexiones aceptadas
- Se actualiza el grafo NetworkX subyacente
- Se imprimen líneas `c` (cableado) o `r` (recableado) a `stdout`
- Se reinician atributos para el nuevo ciclo

---

## Parámetros Configurables

### Topologías iniciales
- **Malla** (`grafo=1`): grid 2D de `ROWS×COLUMNS` (default: 8×8 = 64 nodos)
- **Anillo** (`grafo=3`): grafo circulante de `NODOS_ANILLO` nodos (default: 64)

### Algoritmos de encaminamiento
| Algoritmo | Clave | Descripción |
|-----------|-------|-------------|
| Compass Routing | `CR` | Reenvía al vecino con menor ángulo hacia el destino |
| Shortest Path | `SP` | Calcula ruta más corta vía Dijkstra (usa visión global) |
| Random Walk | `RW` | Camina aleatoriamente hasta [distanciaMaxima](file:///Users/usuario/Repositorios/rewiring/paquete.py#43-46) pasos |

### Reglas de recableado
| Regla | Selección de candidato |
|-------|----------------------|
| R1 | Nodo más visitado en `f_n` (mayor frecuencia) |
| R2 | Primer nodo en `f_n` (orden de descubrimiento) |
| R3 | Selección probabilística proporcional a la frecuencia en `f_n` |

### Otros parámetros
- `ENLACES_DINAMICOS = 2` — enlaces dinámicos por nodo
- `EXPLORADORES = 6` — paquetes exploradores por ciclo
- `CICLOS = 5` — ciclos de reconexión
- `EJECUCIONES = 4` — repeticiones por experimento
- `LONG_ENLACES = [1, 2, 4]` — divisores de longitud máxima de enlace
- `DIV_CONEXIONES = 1` — divisor del máximo de conexiones permitidas

---

## Pipeline de Experimentos

El flujo de trabajo para ejecutar y analizar experimentos se realiza en orden secuencial:

| Paso | Script | Descripción |
|------|--------|-------------|
| 0 | [0creaCopiaSimulador.py](file:///Users/usuario/Repositorios/rewiring/0creaCopiaSimulador.py) | Crea árbol de directorios y copia archivos del simulador a cada carpeta de experimento |
| — | [formacion.py](file:///Users/usuario/Repositorios/rewiring/formacion.py) | Ejecuta [main.py](file:///Users/usuario/Repositorios/rewiring/main.py) + [extractData.py](file:///Users/usuario/Repositorios/rewiring/extractData.py) para cada combinación de parámetros × ejecuciones |
| 1 | [1creaPromediosFormacion.py](file:///Users/usuario/Repositorios/rewiring/1creaPromediosFormacion.py) | Calcula promedios y desviación estándar de AvCl, ASPL y Diámetro → `datos-promedio.csv` |
| 2 | [2creaPromediosDistGradosFormacion.py](file:///Users/usuario/Repositorios/rewiring/2creaPromediosDistGradosFormacion.py) | Promedia distribuciones de grado → `datos-promedio_grados.csv` |
| 3 | [3creaImagenesPNG.py](file:///Users/usuario/Repositorios/rewiring/3creaImagenesPNG.py) | Genera imágenes de grafos (coloreados por grado) e histogramas de distribución de grados |
| 4 | [4creaGEXF.py](file:///Users/usuario/Repositorios/rewiring/4creaGEXF.py) | Exporta grafos finales a formato GEXF (para Gephi) con coordenadas espaciales |
| 5 | [5creaTablasFormacion.py](file:///Users/usuario/Repositorios/rewiring/5creaTablasFormacion.py) | Genera tablas CSV con medidas estructurales consolidadas por combinación de parámetros |

### Estructura de resultados (`ResultadosCN/Formacion/`)
```
Formacion/
├── malla8x8/
│   ├── R1/
│   │   ├── CR/
│   │   │   ├── D1/
│   │   │   │   ├── 1/ ... 4/   (ejecuciones)
│   │   │   │   └── datos-promedio.csv
│   │   │   ├── D2/ ...
│   │   │   └── D4/ ...
│   │   ├── RW/ ...
│   │   └── SP/ ...
│   ├── R2/ ...
│   └── R3/ ...
├── anillo64/ ...
└── Medidas_estructurales/
    └── Medidas_estructurales_*.csv
```

---

## Métricas Extraídas por Experimento

La salida de [extractData.py](file:///Users/usuario/Repositorios/rewiring/extractData.py) registra por cada ciclo:
- **Average Clustering (AvCl)** — coeficiente de agrupamiento promedio
- **Nº Connected Components** — componentes conexas
- **Diameter** — diámetro del grafo
- **Average Shortest Path Length (ASPL)** — longitud de trayectoria promedio
- **Order** — número de nodos

---

## Espacio de Experimentos Actual

Con la configuración en [configuracion.py](file:///Users/usuario/Repositorios/rewiring/configuracion.py), se generan:

| Dimensión | Valores | Total |
|-----------|---------|-------|
| Topologías | malla8x8, anillo64 | 2 |
| Reglas | R1, R2, R3 | 3 |
| Ruteo | SP, CR, RW | 3 |
| Long. enlace | D1, D2, D4 | 3 |
| Ejecuciones | 1–4 | 4 |
| **Total de simulaciones** | | **216** |

---

## Dependencias

- `networkx` — manipulación y análisis de grafos
- `numpy` — cálculos estadísticos (promedios, std, selección probabilística)
- `matplotlib` — generación de imágenes PNG
- Librería estándar: `math`, `random`, `sys`, [os](file:///Users/usuario/Repositorios/rewiring/main.py#65-68), `shutil`, `subprocess`, [re](file:///Users/usuario/Repositorios/rewiring/.DS_Store), `operator`, `pathlib`

### Instalación

```bash
pip install -r requirements.txt
```

---

## Diagramas de Secuencia

### 1. Inicialización del Simulador

```mermaid
sequenceDiagram
    participant M as main.py
    participant Main as Main
    participant NX as NetworkX
    participant Sim as Simulation
    participant Eng as Simulator
    participant P as Process[i]
    participant CN as ComplexNetwork[i]

    M->>Main: __init__()
    Main->>Main: Lee config (nodos, ciclos, grafo)

    alt grafo == 1 (Malla)
        M->>Main: createGrid()
        Main->>NX: grid_2d_graph(rows, cols)
    else grafo == 3 (Anillo)
        M->>Main: createRing()
        Main->>NX: circulant_graph(nodes, [1])
    end

    M->>Sim: Simulation(maxtime, main)
    Sim->>Eng: Simulator(maxtime)
    M->>Sim: readAdjacencyListNetworkX()
    Sim->>NX: graph.nodes(), neighbors()

    loop Para cada nodo i = 1..N
        Sim->>P: Process(neighbors, weights, engine, i)
        M->>CN: ComplexNetwork(main, params...)
        M->>Sim: setModel(CN, i)
        Sim->>P: setModel(CN, port=0)
        P->>CN: setProcess(process, neighbors, weights, id)
        P->>CN: init()
        CN->>CN: creaLongitudEnlacesDinamicos()
    end

    M->>M: Crea Paquete semilla
    M->>Sim: init(Event "PIF-EXPLORACION")
    Sim->>Eng: insertEvent(seed)
    M->>Sim: run()
    
    loop Mientras engine.isOn()
        Sim->>Eng: returnEvent()
        Eng-->>Sim: nextEvent
        Sim->>P: setTime(time)
        Sim->>P: receive(event)
        P->>CN: receive(event)
    end
```

### 2. Fase de Exploración (PIF-EXPLORACION)

```mermaid
sequenceDiagram
    participant C as Nodo Coordinador
    participant A as Nodo A (vecino)
    participant B as Nodo B (lejano)
    participant Eng as Simulator

    Note over C: El coordinador arranca el PIF
    C->>Eng: Event("PIF-EXPLORACION", t, A, C, pkt)
    C->>C: visited = True, father = self

    Note over C: Inicia exploración propia
    C->>C: Crea Paquete explorador (según algoritmo)
    
    alt COMPASS-ROUTING
        C->>C: generaDestino() + Compass_Routing()
    else RANDOM-WALK
        C->>C: distanciaMaxima = random(2, diámetro)
        C->>C: Random_Walk()
    else SHORTEST-PATH
        C->>C: generaDestino() + shortestPath()
    end
    
    C->>Eng: Event("PACKAGE", t+1, nextStep, C, pkt)

    Eng-->>A: PIF-EXPLORACION
    A->>A: visited = True, father = C
    A->>Eng: Propaga PIF a vecinos (excepto padre)
    A->>A: Crea y envía su propio paquete explorador
    A->>Eng: Event("PACKAGE", t+2, nextStep, A, pkt)

    Note over B: Recibe PACKAGE
    Eng-->>B: PACKAGE
    
    alt No llegó al destino
        B->>B: Elimina nodos visitados de vecinos
        B->>Eng: Event("PACKAGE", t+3, nextStep, B, pkt)
    else Llegó al destino o sin vecinos
        B->>B: Invierte ruta del paquete
        B->>Eng: Event("ACK", t+3, prevStep, B, pkt)
    end

    Note over A: Recibe ACK
    Eng-->>A: ACK
    
    alt Falta recorrer ruta
        A->>Eng: Reenvía ACK al siguiente nodo
    else ACK llegó al origen
        A->>A: paquetesRegreso++
        A->>A: Actualiza f_n (frecuencia nodos)
        A->>A: Actualiza f_e (frecuencia enlaces)
        
        alt paquetesRegreso < num_paquetes
            A->>A: Crea nuevo paquete explorador
            A->>Eng: Event("PACKAGE", ...)
        end
    end

    Note over A: Cuando count==0 y todos los ACKs recibidos
    A->>Eng: Event("PIF-EXPLORACION", t, padre, A, null)
    Note over A: Reporta terminación al padre

    Note over C: Coordinador recibe todos los reportes
    C->>C: reiniciaPIF()
    C->>Eng: Event("PIF-NEGOCIACION", t, C, C, null)
    Note over C: Inicia Fase 2
```

### 3. Fase de Negociación (PIF-NEGOCIACION)

```mermaid
sequenceDiagram
    participant C as Coordinador
    participant A as Nodo A (solicitante)
    participant R as Nodo intermedio
    participant B as Nodo B (destino)
    participant Eng as Simulator

    C->>Eng: Event("PIF-NEGOCIACION", t, vecinos, C)
    Note over C: Propaga PIF a todos los vecinos

    Eng-->>A: PIF-NEGOCIACION
    A->>A: visited = True
    A->>Eng: Propaga PIF a sus vecinos

    Note over A: Evalúa f_n para seleccionar candidato

    alt Tiene enlaces dinámicos libres
        A->>A: Reglas.seleccionar_candidato()
        A->>A: Verifica restricción de distancia
        A->>A: Busca ruta más corta en paquetes previos
        A->>Eng: Event("SOLICITUD-CONEXION", t+1, R, A, pkt)
        A->>A: numeroSolicitudes++
    else No tiene enlaces libres
        A->>A: Ordena f_e (menor frecuencia primero)
        alt f_e[menor] < umbral
            A->>A: Reglas.seleccionar_candidato()
            A->>A: Verifica frecuencia y distancia
            A->>Eng: Event("SOLICITUD-CONEXION", t+1, R, A, pkt)
            Note over A: Propone recableado
        else f_e[menor] >= umbral
            Note over A: No hace nada
        end
    end

    Eng-->>R: SOLICITUD-CONEXION
    R->>Eng: Reenvía por la ruta hacia B

    Eng-->>B: SOLICITUD-CONEXION (ruta vacía = llegó)
    
    alt B solicitó a A también (cruce)
        alt B.id > A.id y conexiones < máximo
            B->>Eng: Event("ACEPTO-CONEXION", ...)
            B->>B: neighborsPendientes.add(A)
        else B.id < A.id
            B->>Eng: Event("RECHAZO-CONEXION", ...)
        end
    else B no solicitó a A
        alt conexiones < máximo
            B->>Eng: Event("ACEPTO-CONEXION", ...)
            B->>B: neighborsPendientes.add(A)
        else conexiones >= máximo
            B->>Eng: Event("RECHAZO-CONEXION", ...)
        end
    end

    Eng-->>A: ACEPTO-CONEXION (llega al origen)
    A->>A: numeroSolicitudes--
    A->>A: solicitudesPendientes.add(paquete)
    
    alt Enlace ya conectado (recableado)
        A->>Eng: Event("DESCONEXION", t, nodoViejo, A)
        A->>A: numeroSolicitudes++
        Eng-->>A: DESCONEXION-RECIBIDA
        A->>A: numeroSolicitudes--
    end

    Note over A: Cuando numeroSolicitudes==0 y count==0
    A->>Eng: Event("PIF-NEGOCIACION", padre, A)

    Note over C: Coordinador completa PIF
    C->>Eng: Event("PIF-CONEXION", t, C, C)
    Note over C: Inicia Fase 3
```

### 4. Fase de Conexión (PIF-CONEXION)

```mermaid
sequenceDiagram
    participant C as Coordinador
    participant A as Nodo A
    participant B as Nodo B (desconectado)
    participant NX as Grafo NetworkX
    participant Eng as Simulator

    C->>Eng: Event("PIF-CONEXION", t, vecinos, C)

    Eng-->>A: PIF-CONEXION
    A->>A: visited = True

    Note over A: Materializa conexiones pendientes
    
    alt neighborsPendientes no vacío
        A->>A: neighbors.add(cada pendiente)
    end
    
    alt neighborsPendientesEliminación no vacío
        A->>A: neighbors.remove(cada eliminado)
    end

    loop Para cada solicitud aceptada
        A->>A: Busca enlace dinámico por idEnlace
        alt enlace ya conectado (recableado)
            A->>A: vecinosDinámicos.remove(viejo)
            A->>NX: graph.remove_edge(A, viejo)
            A->>A: print("r A viejo nuevo ciclo")
        else enlace libre (cableado nuevo)
            A->>A: print("c A -1 nuevo ciclo")
        end
        A->>NX: graph.add_edge(A, nuevo)
        A->>A: enlace.idConectado = nuevo
        A->>A: enlace.libre = False
        A->>A: vecinosDinámicos.add(nuevo)
    end

    Note over A: Propaga PIF-CONEXION a vecinos actualizados
    A->>Eng: Event("PIF-CONEXION", vecinos)

    Note over A: Cuando count == 0
    A->>A: contadorCiclos++
    A->>A: reiniciaAtributosParaCicloNuevo()
    A->>Eng: Event("PIF-CONEXION", padre, A)

    Note over C: Coordinador recibe todos los reportes
    C->>C: reiniciaAtributosParaCicloNuevo()
    
    alt contadorCiclos < maxCiclos
        C->>NX: diameter(graph)
        alt diámetro > 2
            C->>Eng: Event("PIF-EXPLORACION", ...)
            Note over C: Nuevo ciclo de reconexión
        else diámetro == 2
            Note over C: Red completamente conexa, detiene simulación
        end
    else ciclos completados
        Note over C: FIN de la simulación
    end
```

### 5. Pipeline de Experimentos

```mermaid
sequenceDiagram
    participant U as Usuario
    participant S0 as 0creaCopiaSimulador
    participant F as formacion.py
    participant Main as main.py
    participant ED as extractData.py
    participant S1 as 1creaPromedios
    participant S2 as 2creaPromDistGrados
    participant S3 as 3creaImagenesPNG
    participant S4 as 4creaGEXF
    participant S5 as 5creaTablas
    participant FS as ResultadosCN/

    U->>S0: Ejecuta paso 0
    S0->>FS: Crea árbol: red/R{n}/ruteo/D{n}/
    S0->>FS: Copia archivos del simulador

    U->>F: Ejecuta formacion.py
    
    loop Por cada combinación (red × regla × ruteo × enlace)
        F->>FS: Genera config.py con parámetros
        loop x = 1..EJECUCIONES
            F->>Main: subprocess.run(main.py)
            Main-->>FS: stdout → salida_x.txt
            F->>ED: subprocess.run(extractData.py, salida_x.txt)
            ED->>FS: datos-salida_x.txt
            ED->>FS: graph_test_ciclo.adjlist
            ED->>FS: hist_test_ciclo.txt
        end
    end

    U->>S1: Ejecuta paso 1
    S1->>FS: Promedia AvCl, ASPL, Diámetro
    S1->>FS: → datos-promedio.csv (con std)

    U->>S2: Ejecuta paso 2
    S2->>FS: Promedia distribuciones de grado
    S2->>FS: → datos-promedio_grados.csv

    U->>S3: Ejecuta paso 3
    S3->>FS: Genera visualización de grafos
    S3->>FS: → img_graph_test_*.png
    S3->>FS: → distGrados*.png

    U->>S4: Ejecuta paso 4
    S4->>FS: Exporta grafos con coordenadas
    S4->>FS: → graph_test_*.gexf

    U->>S5: Ejecuta paso 5
    S5->>FS: Consolida medidas estructurales
    S5->>FS: → Medidas_estructurales/*.csv
```
