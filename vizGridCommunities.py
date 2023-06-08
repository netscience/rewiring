
import sys
import networkx as nx
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

def getCoordinates(nodeId,nodos,contador):
        """calculates the coordinates of an node id according to the grid used by the simulation """
        x = (nodeId-1)%nodos
        coord = [x,contador]
        return coord

def draw_graph(graphFile,nodes):
    # Read graph in graphml format, the graphs to be used are the ones obtained by gephi
    G = nx.read_graphml(graphFile, node_type=int)
    coordenadas=[]
    nodos=int(nodes)*int(nodes)
    contador=int(nodes)-1
    identificador=1
    for i in range(1,int(nodes)+1):
        for j in range(1,int(nodes)+1):
            coordenadas.append(getCoordinates(identificador,int(nodes),contador))
            identificador+=1
        contador-=1
    posicion = dict(zip(sorted(G),coordenadas))  #Association of positions to nodes
    for key in posicion:
        nt = (float(posicion[key][0]*10), float(posicion[key][1] * 10))
        posicion[key]= nt
    fig = plt.figure(num = None, figsize = (10.5,11), dpi = 200)
    ax = plt.subplot()
    ax.axis('off')
    r = nx.get_node_attributes(G, "r")
    g = nx.get_node_attributes(G, "g")
    b = nx.get_node_attributes(G, "b")
    color=[]
    for i in r.keys():
        tupla=(r[i]/255,g[i]/255,b[i]/255)
        color.append(tupla)
    size = [80 for v in G.nodes()]
    #Graficamos nodos y aristas ,with_labels=False
    nodes = nx.draw_networkx_nodes(G,posicion,node_color=color,alpha=0.9,node_size=size,cmap='rainbow',linewidths=0.3,ax=ax)
    nodes.set_edgecolor('#686868')
    #etiquetas=nx.get_node_attributes(G, "Modularity Class")
    #nx.draw_networkx_labels(G, pos=posicion,labels=etiquetas,font_size=5)# draw node labels/names
    cut = 1.00
    xmax = cut * max(xx for xx, yy in posicion.values())
    ymax = cut * max(yy for xx, yy in posicion.values())
    ax.set_xlim(-5.00, xmax+5.00)
    ax.set_ylim(-5.00, ymax+5.00)
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="3%", pad=0.1)
    clb = plt.colorbar(nodes,cax=cax)
    clb.set_label("Grado",size=12)
    clb.ax.tick_params(labelsize=12)
    plt.savefig("img_"+graphFile+".png", dpi=200)
#---------------------------------
#--------------Main---------------
#---------------------------------
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print ("Please supply a file name")
        raise SystemExit(1)
    draw_graph(sys.argv[1],sys.argv[2])