
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
    # Read graph in adjlist format and the position of the nodes in a ring is calculated
    G = nx.read_adjlist(graphFile, comments='#', nodetype=int)
    coordenadas=[]
    nodos=int(nodes)
    for i in range(1,nodos+1):
        coordenadas.append(getCoordinatesAnillo(i,nodos))
    posicion = dict(zip(sorted(G),coordenadas))  #Association of positions to nodes
    fig = plt.figure(num = None, figsize = (30,30), dpi = 200)
    ax = plt.subplot()
    ax.axis('off')
    bet = nx.betweenness_centrality(G,normalized=False)
    claves = bet.keys()
    size = [(float(bet[v]))/10000 for v in claves]
    color = [(float(bet[v])) for v in claves]
    #Graficamos nodos y aristas ,with_labels=False
    nodes = nx.draw_networkx_nodes(G,posicion,node_color=color,alpha=0.9,node_size=size,cmap='rainbow',linewidths=0.3,ax=ax)
    nx.draw_networkx_edges(G,posicion,alpha=0.4,width=0.4,edge_color='#585d5f')
    nodes.set_edgecolor('#686868')
    nx.draw_networkx_labels(G, pos=posicion,labels=bet,font_size=1)# draw node labels/names
    cut = 1.00
    xmax = cut * max(xx for xx, yy in posicion.values())
    ymax = cut * max(yy for xx, yy in posicion.values())
    ax.set_xlim(-10.1, xmax+0.5)
    ax.set_ylim(-10.1, ymax+0.5)
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="3%", pad=0.1)
    clb = plt.colorbar(nodes,cax=cax)
    clb.set_label("betweenness_centrality",size=12)
    clb.ax.tick_params(labelsize=12)
    plt.savefig("betwenness_img_"+graphFile+".png", dpi=500)
#---------------------------------
#--------------Main---------------
#---------------------------------
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print ("Please supply a file name")
        raise SystemExit(1)
    draw_graph(sys.argv[1],sys.argv[2])