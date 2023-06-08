
import sys
import networkx as nx
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import operator

def getCoordinates(nodeId,nodos,contador):
        """calculates the coordinates of an node id according to the grid used by the simulation """
        x = (nodeId-1)%nodos
        coord = [x,contador]
        return coord

def draw_graph(graphFile,nodes):
    # Read graph in adjlist format and the position of the nodes in a grid is calculated
    G = nx.read_adjlist(graphFile, comments='#', nodetype=int)
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
    bet = nx.closeness_centrality(G)
    claves = bet.keys()
    size = [float(bet[v])*1000 for v in claves]
    color = [(float(bet[v])) for v in claves]
    #Graficamos nodos y aristas
    nodes = nx.draw_networkx_nodes(G,posicion,node_color=color,alpha=0.9,node_size=size,cmap='rainbow',linewidths=0.3,ax=ax)
    nx.draw_networkx_edges(G,posicion,alpha=0.4,width=0.4,edge_color='#585d5f')
    nodes.set_edgecolor('#686868')
    nx.draw_networkx_labels(G, pos=posicion,labels=bet,font_size=1)# draw node labels/names
    cut = 1.00
    xmax = cut * max(xx for xx, yy in posicion.values())
    ymax = cut * max(yy for xx, yy in posicion.values())
    ax.set_xlim(-5.00, xmax+5.00)
    ax.set_ylim(-5.00, ymax+5.00)
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="3%", pad=0.1)
    clb = plt.colorbar(nodes,cax=cax)
    clb.set_label("closeness_centrality",size=12)
    clb.ax.tick_params(labelsize=12)
    plt.savefig("closeness_img_"+graphFile+".png", dpi=1000)
#---------------------------------
#--------------Main---------------
#---------------------------------
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print ("Please supply a file name")
        raise SystemExit(1)
    draw_graph(sys.argv[1],sys.argv[2])