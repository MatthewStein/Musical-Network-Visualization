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
  

# Given list of parts condensed to notes and chords, generate a list of edges
# where each node is defined by the given list of properties: 
#    []
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
                
                if len(attr) == 1:
                    reduced.append(attr[0])
                else:
                    reduced.append(tuple(attr))
            
        for j in range(len(part)-1):
            edge = (reduced[j], reduced[j+1])
            edges[edge] = edges.get(edge, 0) + 1
    
    return edges

  
def generateNetwork(edges, directed=False, weighted=True, (min_width, max_width)=(0.3,1)):
    if directed:
        G = nx.DiGraph()
    else:
        G = nx.Graph()
        
    max_occ = max(edges.itervalues())
    for key, value in edges.iteritems():
        (note1, note2) = key
        G.add_edge(note1, note2, weight=float(value)/max_occ)
    
    # should make pos a param also
    pos = nx.circular_layout(G)
    
    # draw edges -> width = min + (max-min)*weight
    for (u,v,d) in G.edges(data=True):
        nx.draw_networkx_edges(G, pos, [(u,v)], 
            min_width + (max_width-min_width)*d['weight'])
    nx.draw_networkx(G, pos, edgelist=[], with_labels=True, node_size=600)
    plt.show()


############################################################################

parts = scoreToParts("bach/bwv57.8")

edges_min = musicalEdgeList(parts, ["name"])
edges_max = musicalEdgeList(parts, ["nameOct", "duration"])

generateNetwork(edges_min, False, True, (0.3,7))
#generateNetwork(edges_max, False, True, (0.3,7))