
import sys
import networkx as nx
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import math

def getCoordinatesAnillo(nodeId,nodos):
    #transformacion de coordenadas polares a rectangulares:
    angulo = math.radians((360/nodos)*nodeId)#la función math.radians() convierte los grados sexagesimales en radianes
    x = 10*math.cos(angulo)#se asume que el anillo tiene radio 10
    y = 10*math.sin(angulo)#se asume que el anillo tiene radio 10
    coord = (x,y)
    #print("soy",nodeId,"mis coordenadas son",coord)
    return coord

def draw_graph(graphFile,nodes):
    # Read graph in graphml format, the graphs to be used are the ones obtained by gephi
    G = nx.read_graphml(graphFile, node_type=int)
    coordenadas=[]
    nodos=int(nodes)
    for i in range(1,nodos+1):
        coordenadas.append(getCoordinatesAnillo(i,nodos))
    posicion = dict(zip(sorted(G),coordenadas))  #Association of positions to nodes
    fig = plt.figure(num = None, figsize = (30,30), dpi = 200)
    ax = plt.subplot()
    ax.axis('off')
    r = nx.get_node_attributes(G, "r")
    g = nx.get_node_attributes(G, "g")
    b = nx.get_node_attributes(G, "b")
    color=[]
    for i in  r.keys():
        tupla=(r[i]/255,g[i]/255,b[i]/255)
        color.append(tupla)
    size = [500 for v in G.nodes()]
    #Graficamos nodos y aristas ,with_labels=False
    nodes = nx.draw_networkx_nodes(G,posicion,node_color=color,alpha=0.9,node_size=size,cmap='rainbow',linewidths=0.3,ax=ax)
    nx.draw_networkx_edges(G,posicion,alpha=0.4,width=0.4,edge_color='#585d5f')
    nodes.set_edgecolor('#686868')
    #etiquetas=nx.get_node_attributes(G, "Modularity Class")
    #nx.draw_networkx_labels(G, pos=posicion,labels=etiquetas,font_size=5)# draw node labels/names
    cut = 1.00
    xmax = cut * max(xx for xx, yy in posicion.values())
    ymax = cut * max(yy for xx, yy in posicion.values())
    ax.set_xlim(-10.1, xmax+0.5)
    ax.set_ylim(-10.1, ymax+0.5)
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