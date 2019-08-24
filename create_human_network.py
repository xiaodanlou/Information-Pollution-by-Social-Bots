#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
@author: rosdays

@description: create human network
"""

from __future__ import division
import matplotlib as mpl
mpl.use('Agg')

import os
import sys
import random
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

from collections import Counter


if nx.__version__ != "1.11":
    raise ImportError, "`networkx` version should be 1.11"

class DirectedHighCluster_out(object):

    def __init__(self, n, m=3, p=0.5):
        self.n = n
        self.m = m
        self.p = p
        self.G = nx.DiGraph()

    def generate(self):
        self.G.add_edges_from([(0,1),(0,2),(0,3),(1,0),(1,2),(1,3),(2,0),(2,1),(2,3),(3,1),(3,2),(3,0)])
        source = self.m + 1 # original 4 points
        while source < self.n:
            target = random.choice(self.G.nodes())
            self.G.add_edge(source, target)
            rest = 1
            while rest < self.m:
               # trial
                temp = random.random()
                if temp <= self.p:
                    neighbors = self.G.neighbors(target) # only out-degree neighbors ( same as self.G.successors(target) )
                    filte_neighbors = [nei for nei in neighbors if not self.G.has_edge(source, nei)]
                    if len(filte_neighbors) > 0:
                        target_nei = random.choice(filte_neighbors)
                        self.G.add_edge(source, target_nei)
                        rest += 1
                else:
                    # attach
                    current_nodes = [node for node in self.G.nodes() if source != node]
                    target_nodes = [c_node for c_node in current_nodes if not self.G.has_edge(source, c_node)]
                    if len(target_nodes) > 0:
                        target = random.choice(target_nodes)
                        self.G.add_edge(source, target)
                        rest += 1

            source += 1

        return self.G

def rewire_outdegree_edge(G_old):
    print "rewire: 断1条边并重连1条边--选择入度=0的节点重连，入度大于1的节点断边"
    g = nx.DiGraph(G_old)
    zero_indegree_node = [k[0] for k in g.in_degree().items() if k[1] == 0]
    for node in zero_indegree_node:
        fil = [k[0] for k in g.in_degree().items() if k[1] > 1]
        target = random.choice(fil)
        sour = random.choice(g.predecessors(target))
        while sour == node:
            sour = random.choice(g.predecessors(target))
        g.remove_edge(sour, target)
        g.add_edge(sour, node)
    return g


if len(sys.argv) < 3:
    print "usage: %s <n> <m> <p>" % __file__
    sys.exit(0)

#========== PARAMETERS ==========
n = int(sys.argv[1])
m = int(sys.argv[2])
p = float(sys.argv[3])
#========= END PARAMETERS =========

G = DirectedHighCluster_out(n, m, p).generate()
networkFile = './gmls/directedHighCluster_{}_{}_{}.gml'.format(n, m, p) # gml format network save file
if not os.path.exists(networkFile): # create, then save it for other percent_bot
   print 'Creating network, then save it...'
   G = DirectedHighCluster_out(n, m, p).generate()
   nx.write_gml(G, networkFile)
else:
   print 'Loading network...'
   G = nx.read_gml(networkFile)

G_rewire = rewire_outdegree_edge(G)
nx.write_gml(G_rewire, './gmls/directedHighCluster_{}_{}_{}_rewire.gml'.format(n, m, p))

g_in =  G.in_degree()
g_rewire_in =  G_rewire.in_degree()
g_out =  G.out_degree()
g_rewire_out =  G_rewire.out_degree()

fp = open("result_{}_{}_{}.txt".format(n, m, p), "w")
print >> fp, "    \t\t in_degree \t\t out_degree"
print >> fp, "Node\t\Ori\tRewire\t\Ori\tRewire"
for node in G.nodes():
    print >> fp, "{}\t\t{}\t{}\t\t{}\t{}".format(node, g_in[node], g_rewire_in[node], g_out[node], g_rewire_out[node])
fp.close()

cnt = Counter(g_in.values())
xs, ys = cnt.keys(), cnt.values()
ys = np.array(ys)*1.0 / np.sum(ys)
plt.loglog(xs, ys, '*', label='original')

cnt = Counter(g_rewire_in.values())
xs, ys = cnt.keys(), cnt.values()
ys = np.array(ys)*1.0 / np.sum(ys)
plt.loglog(xs, ys, 'o', label='rewire')
plt.title('in-degree distribution')

plt.legend(loc='best')
plt.savefig('directedHCOut_indegree_distr_{}_{}_{}.png'.format(n, m, p))
plt.close()
