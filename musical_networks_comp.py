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
                
                if "name" in properties:
                    attr.append(n.name)
                if "nameOct" in properties:
                    attr.append(n.nameWithOctave)
                if "duration" in properties:
                    attr.append(n.quarterLength)
                
                if len(attr) == 1:
                    reduced.append(attr[0])
                else:
                    reduced.append(tuple(attr))
            
        for j in range(len(part)-1):
            edge = (reduced[j], reduced[j+1])
            edges[edge] = edges.get(edge, 0) + 1
    
    return edges
            
  
def generateNetwork(edges, directed=False, weighted=True):
  return 0

############################################################################

parts = scoreToParts("bach/bwv57.8")

edges_min = musicalEdgeList(parts, ["name"])
edges_max = musicalEdgeList(parts, ["nameOct", "duration"])


# MINIMAL NETWORK
# should make into DiGraph()
G_min = nx.Graph()
max_occ = max(edges_min.itervalues())
for key, value in edges_min.iteritems():
    (note1, note2) = key
    G_min.add_edge(note1, note2, weight=float(value)/max_occ)
    
pos=nx.circular_layout(G_min)
#nx.draw_networkx_nodes(G_min, pos, with_labels=True, node_size=600)

cutoff = 0.4
elarge=[(u,v) for (u,v,d) in G_min.edges(data=True) if d['weight'] > cutoff]
esmall=[(u,v) for (u,v,d) in G_min.edges(data=True) if d['weight'] <= cutoff]

nx.draw_networkx_edges(G_min,pos,edgelist=elarge,width=3)
nx.draw_networkx_edges(G_min,pos,edgelist=esmall,width=3,alpha=0.5,edge_color='b',style='dashed')
nx.draw_networkx(G_min, pos, edgelist=[], with_labels=True, node_size=600)
plt.show()


# MAXIMAL NETWORK 
G_max = nx.Graph()
for key, value in edges_max.iteritems():
    (note1, note2) = key
    G_max.add_edge(note1, note2)
    # also, value = weight
#nx.draw(G_max)
#plt.show()