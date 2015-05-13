# Comparative Analysis of Musical Network Representations
# Matthew Stein & Ryan Gourley
# May 2015

from music21 import *
import networkx as nx
import matplotlib.pyplot as plt

###############################################################
# Convert a score in the Music21 corpus into a list of Parts, #
#   each which is a flattened Stream of Notes and/or Chords   #
###############################################################

def scoreToParts(music, reduce_type="both"):
    score = corpus.parse(music)
    parts = score.parts
    numParts = len(parts)
    
    note_stream = []
    
    for i in range(numParts):
        if reduce_type == "note":
            note_stream.append(parts[i].flat.getElementsByClass('Note'))
        elif reduce_type == "chord":
            note_stream.append(parts[i].flat.getElementsByClass('Chord'))
        else:
            note_stream.append(parts[i].flat.getElementsByClass(['Note', 'Chord']))
        
    return note_stream
  

###############################################################
# Generate a list of edges and frequences of occurence where  #
#   each node is defined by the given list of properties.     #
###############################################################

def musicalEdgeList(parts, properties, part_type="note"):
    edges = {}
    
    for part in parts:
        reduced = []
        if part_type == "note":
            for i in range(len(part)):
                n = part[i]
                attr = []
                
                if "name" in properties:      attr.append(n.name)
                if "nameOct" in properties:   attr.append(n.nameWithOctave)
                if "duration" in properties:  attr.append(n.quarterLength)
                if "freq" in properties:      attr.append(n.frequency)
                
                if len(attr) == 1:
                    reduced.append(attr[0])
                else:
                    reduced.append(tuple(attr))
            
        for j in range(len(part)-1):
            edge = (reduced[j], reduced[j+1])
            edges[edge] = edges.get(edge, 0) + 1
    
    return edges

###############################################################
# Draw a network consisting of nodes representing notes or    #
#  chords and edges as horizontal connections between them.   #
###############################################################
  
def generateNetwork(edges, directed=False, weighted=True, (min_width, max_width)=(0.3,1), layout="spring"):
    if directed:
        G = nx.DiGraph() # how to get nicer arrows for directed network?
    else:
        G = nx.Graph()
    
    max_occ = max(edges.itervalues())
    for key, value in edges.iteritems():
        (note1, note2) = key
        G.add_edge(note1, note2, weight=float(value)/max_occ)
    
    if layout == "spring":
        pos = nx.spring_layout(G, k=0.25, iterations=55)
    elif layout == "circle":
        pos = nx.circular_layout(G)
    
    for (u,v,d) in G.edges(data=True):
        nx.draw_networkx_edges(G, pos, [(u,v)], 
            min_width + (max_width - min_width) * d['weight'])
    nx.draw_networkx(G, pos, edgelist=[], with_labels=True, node_size=600)
    
    plt.savefig("bach_octave.png")
    plt.show()

############################################################################

bach = scoreToParts("bach/bwv57.8")

edges_min = musicalEdgeList(bach, ["name"])
edges_max = musicalEdgeList(bach, ["nameOct", "duration"])

generateNetwork(edges_min, False, True, (0.3,16), layout="circle")
#generateNetwork(edges_max, False, True, (0.3,7))