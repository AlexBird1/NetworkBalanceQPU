import networkx as nx
import random
import time

G = nx.complete_graph(3) # this section creates a randomly signed network with 4 nodes
G.add_edges_from([(u, v, {'sign': 2*random.randint(0, 1)-1}) for u, v in G.edges])
nx.relabel_nodes(G, {0: 'U1', 1: 'U2', 2: 'U3'}, copy=False)

print('Friendly relationships: ', [(x, y) for (x, y, sign) in G.edges(data='sign') if (sign == 1)])
print('Hostile relationships: ', [(x, y) for (x, y, sign) in G.edges(data='sign') if (sign == -1)])

start = time.perf_counter() #starting the timer 

from solvers import default_solver #this section creates and runs the solver 
my_solver, my_token = default_solver()

from dwave.system.samplers import DWaveSampler
from dwave.system.composites import EmbeddingComposite

sampler = EmbeddingComposite(DWaveSampler(solver={'qpu': True}))

import dwave_networkx as dnx
imbalance, bicoloring = dnx.structural_imbalance(G, sampler)

for edge in G.edges:
    G.edges[edge]['frustrated'] = edge in imbalance
for node in G.nodes:
    G.nodes[node]['color'] = bicoloring[node]

fin = time.perf_counter() # solver is complete so stop timer

print('Group1: ', [person for (person, color) in bicoloring.items() if (color == 0)])
print('Group2: ', [person for (person, color) in bicoloring.items() if (color == 1)])
print('\nFrustrated relationships: ', list(imbalance.keys()))
print(f"Network balanced in {fin - start:0.4f} seconds")
