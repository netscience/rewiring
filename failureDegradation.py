  
import sys
import networkx as nx
import random
import collections

def create_datafile():
    """Crea el archivo donde se almacenarán los datos de la degradación"""
    with open (ruta+'degradationData.txt','w') as data:
        data.write('{} {} {} {} {} {} {} {} {}'.format("#n_nodes","m_edges","aspl","diameter","acluster","assort","n_conn","n_comp","o_largestc\n"))

def create_histogramsfile():
    with open (ruta+'degreeHistograms.txt','w') as histograms:
        histograms.write('{}'.format("# n  list(x)  list(y)\n"))


def save_degree_histogram(D):
    """Guarda los datos necesarios para gnerar el histograma de grados del grafo que recibe"""
    degree_sequence = sorted([d for n, d in D.degree()], reverse=True)  # degree sequence
    #print ("Degree sequence", degree_sequence)
    degreeCount = collections.Counter(degree_sequence)
    #print ("Degree count", degreeCount)
    deg, cnt = zip(*degreeCount.items())
    #print ("deg = ",deg," cnt = ",cnt)
    with open(ruta+'degreeHistograms.txt','a') as histograms:
        histograms.write('{:>2}'.format(len(deg)))
        for d in deg:
            histograms.write('{:>5}'.format(d))
        for c in cnt:
            histograms.write('{:>5}'.format(c))
        histograms.write('{}'.format('\n'))
        

def graph_properties(G):
    """ Calcula y guarda las propiedades del grafo G """
    n_nodes = G.order()                                    # Numero de vertices
    m_edges = G.size()                                     # Numero de aristas
    components = nx.connected_components(G)                # Componentes conectados de G
    n_components = nx.number_connected_components(G)       # Numero de componentes conectados
    largest_cc = max(nx.connected_components(G), key=len)  # Componente más grande
    L = G.subgraph(largest_cc)                             # Grafo que descibe al componente más grande
    order_L = L.order()                                    # Numero de nodos en el componente más grande
    if n_components > 1:       # Si hay más de un componente calculas las propiedades para el más grande
        aspl = nx.average_shortest_path_length(L)          # Longitud de trayectoria más corta promedio
        diameter = nx.diameter(L)                          # Diametro 
        a_clustering = nx.average_clustering(L)            # Coeficiente de agrupamiento promedio
        node_connectivity = nx.node_connectivity(L)        # Conectividad por nodo
        if (order_L>2):
            try:
                assortativity = nx.degree_pearson_correlation_coefficient(L)    # Coeficiente de asortatividad
            except RuntimeWarning:
                assortativity = 'na'
            save_degree_histogram(L)
        else:
            assortativity = 'na'
        
    else:                      # Otro Sigo calculando las propiedades para el grafo G
        aspl = nx.average_shortest_path_length(G)
        diameter = nx.diameter(G)
        a_clustering = nx.average_clustering(G)
        node_connectivity = nx.node_connectivity(G)
        if (n_nodes>2):
            try:
                assortativity = nx.degree_pearson_correlation_coefficient(G)
            except RuntimeWarning:
                assortativity = 'na'            
            save_degree_histogram(G)
        else:
            assortativity = 'na'
    if assortativity!='na':   
        with open (ruta+'degradationData.txt','a') as data:
            data.write('{:>4} {:>6} {:>10f} {:>4} {:>10f} {:>10f} {:>3} {:>4} {:>6} {}'.format(n_nodes,m_edges,aspl,diameter,a_clustering,assortativity,node_connectivity,n_components,order_L,"\n"))
    else:
        with open (ruta+'degradationData.txt','a') as data:
            data.write('{:>4} {:>6} {:>10f} {:>4} {:>10f} {:>10} {:>3} {:>4} {:>6} {}'.format(n_nodes,m_edges,aspl,diameter,a_clustering,assortativity,node_connectivity,n_components,order_L,"\n"))

def failure_degradation():
    """Degrada un grafo hasta que ya no tiene nodos, simulando fallos aleatorios"""
    save_step=0.01  #Guardamos datos cada que elimino x% de los nodos
    deleted_nodes = []
    initial_order = G.order()
    cont = 0
    create_datafile()
    graph_properties(G)
    create_histogramsfile()
    save_degree_histogram(G)
    while G.order() > 1:
        random_node = random.choice(list(G))
        G.remove_node(random_node)
        deleted_nodes.append(random_node)
        cont += 1
        if ((cont == (initial_order*save_step)) or (G.order()==1)):
            graph_properties(G)
            cont = 0
    with open (ruta+'FailureSequence.txt','w') as seq:
        for node in deleted_nodes:
            seq.write('{}{}'.format(node,"\n"))
 
#--------------------------------------
#-----------------Main-----------------
#--------------------------------------
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print ("Please supply a file name")
        raise SystemExit(1)
    ruta=sys.argv[2]
    # The program receives a graph in networkx adjlist format
    print("la ruta es",ruta)
    print("la ruta total es",ruta+sys.argv[1])
    G = nx.read_adjlist(ruta+sys.argv[1],comments='#',nodetype=int)
    failure_degradation()