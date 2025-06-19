import networkx as nx


# Crear malla de 50x50
grid_size = 50
grid_graph = nx.grid_2d_graph(grid_size, grid_size)

# Guardar como lista de adyacencia
nx.write_adjlist(grid_graph, "malla.adjlist")

# Crear anillo de 1500 nodos
cycle_graph = nx.cycle_graph(1500)

# Guardar como lista de adyacencia
nx.write_adjlist(cycle_graph, "anillo.adjlist")

print("Archivos guardados: malla.adjlist y anillo.adjlist")