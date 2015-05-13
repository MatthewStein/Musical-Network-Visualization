# Comparative Analysis of Musical Network Representations
# Matthew Stein & Ryan Gourley
# May 2015

from music21 import *
import networkx as nx
import matplotlib.pyplot as plt

bach = corpus.parse('bach/bwv57.8')

# flatten individual parts to streams of just Notes
soprano = bach[1].flat.getElementsByClass('Note')
alto = bach[2].flat.getElementsByClass('Note')
tenor = bach[3].flat.getElementsByClass('Note')
bass = bach[4].flat.getElementsByClass('Note')

parts = [soprano, alto, tenor, bass]

# consider only note name, ignore octave and duration
edges_min = {}
# distinct node for each note of specific name, octave, and duration
edges_max = {}

for part in parts:
  reduced_min = []
  reduced_max = []

  for i in range(len(part)):
    n = part[i]
    reduced_min.append(n.name)
    reduced_max.append((n.nameWithOctave, n.quarterLength))
        
  for j in range(len(part)-1):
    edge_min = (reduced_min[j], reduced_min[j+1])
    edges_min[edge_min] = edges_min.get(edge_min, 0) + 1
        
    edge_max = (reduced_max[j], reduced_max[j+1])
    edges_max[edge_max] = edges_max.get(edge_max, 0) + 1
    
#print edges_min
#print edges_max

###################
# MINIMAL NETWORK #
###################
### should make into DiGraph()
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

###################
# MAXIMAL NETWORK #
###################
G_max = nx.Graph()
for key, value in edges_max.iteritems():
    (note1, note2) = key
    G_max.add_edge(note1, note2)
    # also, value = weight
#nx.draw(G_max)
#plt.show()