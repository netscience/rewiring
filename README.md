# Rewiring: Simulador de Reconexión Distribuida en Redes Complejas

Simulador de eventos discretos para **modelos de reconexión distribuida en redes complejas**, desarrollado en el marco del proyecto de Ciencia de Frontera **"Modelos de reconexión para la autoorganización de redes complejas de gran escala" (CBF-2025-G-1812)**, apoyado por la Secretaría de Ciencia, Humanidades, Tecnología e Innovación (SECIHTI).

---

## I. Instalación

1. Crear un ambiente de Python (se recomienda Anaconda).
2. Clonar el repositorio:
   ```bash
   git clone https://github.com/netscience/rewiring.git
   cd rewiring
   ```
3. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```

### Dependencias
- `networkx` — creación y análisis de grafos
- `numpy` — cálculos estadísticos (promedios, desviación estándar, selección probabilística)
- `matplotlib` — generación de imágenes PNG

### Configuración de rutas

Modificar `configuracion.py` para indicar la ruta de la carpeta de resultados:

```python
BASE_DIR = str(home_path) + "/Documents/Repositorios/ResultadosCN/"
RESULTADOS_DIR = BASE_DIR + "Formacion"
```

Se recomienda crear un directorio exclusivo para los resultados considerando la ruta relativa al home del usuario.

---

## II. Experimentos de formación de redes

### Configuración de parámetros

Todos los parámetros se definen en `configuracion.py`:

| Parámetro | Variable | Valores por defecto | Descripción |
|-----------|----------|-------------------|-------------|
| Topología inicial | `RED` | `["malla", "anillo"]` | Malla 2D o anillo circulante |
| Orden de la topología | `ROWS`, `COLUMNS`, `NODOS_ANILLO` | 8×8, 64 | Número de nodos |
| Regla de reconexión | `REGLAS` | `[1, 2, 3]` | R1, R2 o R3 |
| Algoritmo de ruteo | `ROUTING` | `["SHORTEST-PATH", "COMPASS-ROUTING", "RANDOM-WALK"]` | SP, CR o RW |
| Longitud de enlace | `LONG_ENLACES` | `[1, 2, 4]` | Divisores de la longitud máxima (D, D/2, D/4) |
| Ciclos de reconexión | `CICLOS` | `5` | Número de ciclos por simulación |
| Ejecuciones | `EJECUCIONES` | `4` | Repeticiones por configuración |
| Enlaces dinámicos | `ENLACES_DINAMICOS` | `2` | Enlaces dinámicos por nodo |
| Exploradores | `EXPLORADORES` | `6` | Paquetes exploradores por nodo y ciclo |
| Máx. conexiones | `DIV_CONEXIONES` | `1` | Divisor del máximo de conexiones (nodos/DIV) |

### Ejecución del pipeline

El flujo de trabajo se ejecuta en orden secuencial:

| Paso | Script | Descripción |
|------|--------|-------------|
| 1 | `0creaCopiaSimulador.py` | Crea el árbol de directorios y copia los scripts del simulador |
| 2 | `formacion.py` | Ejecuta `main.py` + `extractData.py` para cada combinación de parámetros |
| 3 | `1creaPromediosFormacion.py` | Calcula promedios y desviación estándar → `datos-promedio.csv` |
| 4 | `2creaPromediosDistGradosFormacion.py` | Promedia distribuciones de grado → `datos-promedio_grados.csv` |
| 5 | `3creaImagenesPNG.py` | Genera imágenes de grafos e histogramas de distribución de grados |
| 6 | `4creaGEXF.py` | Exporta grafos a formato GEXF (para Gephi con geoLayout) |
| 7 | `5creaTablasFormacion.py` | Genera tablas CSV consolidadas en `Formacion/Medidas_estructurales/` |

> **Nota:** Antes de ejecutar los pasos 5–7, configurar `NODE_SCALE` en `configVisualizacion.py`:
> - `NODE_SCALE = 1` para anillo ≈ 1500 nodos y malla ≈ 2500 nodos
> - `NODE_SCALE = 20` para anillo ≈ 50 nodos y malla ≈ 64 nodos

### Estructura de resultados

```
ResultadosCN/Formacion/
├── malla8x8/
│   ├── R1/
│   │   ├── CR/
│   │   │   ├── D1/
│   │   │   │   ├── config.py
│   │   │   │   ├── 1/ ... 4/          ← ejecuciones
│   │   │   │   │   ├── salida_x.txt
│   │   │   │   │   ├── datos-salida_x.txt
│   │   │   │   │   ├── graph_test_*.adjlist
│   │   │   │   │   └── hist_test_*.txt
│   │   │   │   ├── datos-promedio.csv
│   │   │   │   └── datos-promedio_grados.csv
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

### Métricas extraídas

Para cada ciclo de reconexión, `extractData.py` genera:

| Métrica | Descripción |
|---------|-------------|
| **AvCl** | Coeficiente de agrupamiento promedio |
| **ASPL** | Longitud de trayectoria promedio (Average Shortest Path Length) |
| **Diámetro** | Diámetro del grafo |
| **Componentes** | Número de componentes conexas |
| **Orden** | Número de nodos |

### Espacio de experimentos

Con la configuración por defecto se generan:

| Dimensión | Valores | Cantidad |
|-----------|---------|----------|
| Topologías | malla8x8, anillo64 | 2 |
| Reglas | R1, R2, R3 | 3 |
| Ruteo | SP, CR, RW | 3 |
| Long. enlace | D1, D2, D4 | 3 |
| Ejecuciones | 1–4 | 4 |
| **Total** | | **216 simulaciones** |

---

## III. Arquitectura del simulador

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
        CN["ComplexNetwork<br/>Algoritmo de reconexión"]
        PKG["Paquete<br/>Paquete explorador"]
        ENC["Encaminamiento<br/>Algoritmos de ruteo"]
        ENL["Enlace<br/>Enlace dinámico"]
        REG["Reglas<br/>Reglas de recableado"]
    end

    subgraph "Configuración"
        CONF["configuracion.py<br/>Parámetros del experimento"]
        CONFV["configVisualizacion.py<br/>Parámetros de visualización"]
    end

    subgraph "Pipeline de Ejecución"
        S0["0creaCopiaSimulador.py"]
        FORM["formacion.py"]
        S1["1creaPromediosFormacion.py"]
        S2["2creaPromediosDistGradosFormacion.py"]
        S3["3creaImagenesPNG.py"]
        S4["4creaGEXF.py"]
        S5["5creaTablasFormacion.py"]
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

### Componentes del simulador

#### Motor de simulación de eventos discretos

| Archivo | Responsabilidad |
|---------|-----------------|
| `simulator.py` | Motor con agenda ordenada por tiempo. Inserta/extrae eventos en orden causal |
| `simulation.py` | Orquesta el experimento: lee el grafo, crea procesos, ejecuta el bucle principal |
| `process.py` | Entidad activa en cada nodo. Asocia modelos y reenvía eventos |
| `model.py` | Clase abstracta base con métodos `init()`, `receive()`, `send()` |
| `event.py` | Encapsula: nombre, tiempo, destino, fuente, paquete, puerto |

#### Modelo de reconexión distribuida

| Archivo | Responsabilidad |
|---------|-----------------|
| `complexNetwork.py` | **Núcleo del simulador**. Implementa las 3 fases del ciclo de reconexión |
| `paquete.py` | Paquete explorador: lleva ruta, destino, distancia máxima, ID de enlace |
| `encaminamiento.py` | 3 algoritmos de ruteo + cálculo de distancias en malla y anillo |
| `enlace.py` | Enlace dinámico: ID, longitud máxima, estado libre/ocupado, nodo conectado |
| `reglas.py` | 3 reglas de selección de candidato a reconexión |

---

## IV. Algoritmo de reconexión

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

### Algoritmos de encaminamiento

| Algoritmo | Clave | Descripción |
|-----------|-------|-------------|
| Compass Routing | `CR` | Reenvía al vecino con menor ángulo hacia el destino |
| Shortest Path | `SP` | Calcula ruta más corta vía Dijkstra (usa visión global) |
| Random Walk | `RW` | Camina aleatoriamente hasta `distanciaMaxima` pasos |

### Reglas de recableado

| Regla | Selección de candidato |
|-------|----------------------|
| R1 | Nodo más visitado en `f_n` (mayor frecuencia) |
| R2 | Primer nodo en `f_n` (orden de descubrimiento) |
| R3 | Selección probabilística proporcional a la frecuencia en `f_n` |

---

## V. Diagramas de secuencia

### 1. Inicialización del simulador

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

### 2. Fase de exploración (PIF-EXPLORACION)

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

### 3. Fase de negociación (PIF-NEGOCIACION)

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

### 4. Fase de conexión (PIF-CONEXION)

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

### 5. Pipeline de experimentos

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
