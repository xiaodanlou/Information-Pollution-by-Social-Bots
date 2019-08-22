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


# 全部随机选择
def rewire_outdegree_edge0(G_old, ratio=1.0):
    G = nx.DiGraph(G_old)
    nodes = G.nodes()
    random.shuffle(nodes)
    choosen_nodes = nodes[:int(len(nodes)*ratio)] # random choose `ratio` of nodes to rewire
    for cn in choosen_nodes:
        # 1. remove
        outdegree_nodes = G.successors(cn)
        target_node = random.choice(outdegree_nodes)
        G.remove_edge(cn, target_node)

        # 2. rewire
        target_node = random.choice(nodes)
        while target_node == cn:
            target_node = random.choice(nodes)

        G.add_edge(cn, target_node)

    return G

# 选择前10%节点断边和后10%节点连边
def rewire_outdegree_edge1(G_old, ratio=0.1):
    print "rewire1: 选择前10%节点断边和后10%节点连边"
    G = nx.DiGraph(G_old)
    nodes = G.nodes()
    small_nodes = nodes[:int(len(nodes)*ratio)] # random choose `ratio` of nodes to rewire
    big_nodes =  nodes[-int(len(nodes)*ratio):]

    for sn in small_nodes:
        # 1. remove
        outdegree_nodes = G.successors(sn)
        target_node = random.choice(outdegree_nodes)
        G.remove_edge(sn, target_node)

        # 2. rewire
        target_node = random.choice(big_nodes)
        while target_node == sn:
            target_node = random.choice(big_nodes)
        G.add_edge(sn, target_node)

    return G

def rewire_outdegree_edge2(G_old, ratio=0.0):
    print "rewire2: 断1条边并重连1条边--选择入度=0的节点重连，入度大于1的节点断边"
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

def rewire_outdegree_edge4(G_old, ratio=0.0):
    print "rewire4: 新增2条边--选择入度<2的节点连边，随机挑非自己的2个节点连接"
    g = nx.DiGraph(G_old)
    zero_indegree_node = [k[0] for k in g.in_degree().items() if k[1] < 2]
    for node in zero_indegree_node:
        fil = G_old.nodes()
        sours = random.sample(fil, 2) # choose 2 uique source node
        while node in sours:
            sours = random.sample(fil, 2)

        g.add_edges_from(zip(sours, len(sours)*[node]))

    return g

def rewire_outdegree_edge5(G_old, ratio=0.0):
    print "rewire5: 断2条边并重连2条边--选择入度<2的节点重连，入度大于3的节点断边"
    g = nx.DiGraph(G_old)
    zero_indegree_node = [k[0] for k in g.in_degree().items() if k[1] < 2]
    for node in zero_indegree_node:
        fil = [k[0] for k in g.in_degree().items() if k[1] > 3] # need break 2 edges, so change to 3
        target = random.choice(fil)

        sours = random.sample(g.predecessors(target), 2) # choose 2 uique source node
        while node in sours:
            sours = random.sample(g.predecessors(target), 2)

        g.remove_edges_from(zip(sours, len(sours)*[target]))
        g.add_edges_from(zip(sours, len(sours)*[node]))

    return g

def rewire_outdegree_edge6(G_old, ratio=0.0):
    print "rewire6: 新增1条边--选择入度<2的节点连边，随机挑非自己的1个节点连接"
    g = nx.DiGraph(G_old)
    zero_indegree_node = [k[0] for k in g.in_degree().items() if k[1] < 2]
    for node in zero_indegree_node:
        fil = G_old.nodes()
        sour = random.choice(fil) # choose 1 uique source node
        while node == sour:
            sour = random.choice(fil)

        g.add_edge(sour, node)

    return g

def rewire_outdegree_edge7(G_old, ratio):
    print "rewire7: 随机翻转边"
    g = nx.DiGraph(G_old)
    for edge in g.edges():
        temp = random.random()
        if temp <= ratio:
            g.add_edge(edge[1],edge[0])
            g.remove_edge(edge[0],edge[1])
    return g

def rewire_outdegree_edge8(G_old, ratio=0.0):
    print "rewire8: 随机连边直至变为强连通图(允许双向连边)"
    g = nx.DiGraph(G_old)
    while not nx.is_strongly_connected(g):
        two_nodes = random.sample(g.nodes(), 2) # random choose 2 uique nodes

        g.add_edge(two_nodes[0],two_nodes[1])
    return g

def rewire_outdegree_edge9(G_old, ratio=0.0):
    print "rewire9: 随机连边直至变为强连通图(不允许双向连边)"
    g = nx.DiGraph(G_old)
    while not nx.is_strongly_connected(g):
        two_nodes = random.sample(g.nodes(), 2) # random choose 2 uique nodes
        if g.has_edge(two_nodes[0], two_nodes[1]) or g.has_edge(two_nodes[1], two_nodes[0]):
            continue
        g.add_edge(two_nodes[0],two_nodes[1])
    return g

def rewire_method_proxy(mid):
    assert (mid in [0,1,2,4,5,6,7,8,9]), "Rewire{} not support".format(mid)
    return globals()["rewire_outdegree_edge"+str(mid)]


if len(sys.argv) < 5:
    print "usage: %s <node> <p> <rewire_ratio> <method_id>" % __file__
    sys.exit(0)

m = 3
percent_bot = 0.1
node = int(sys.argv[1])
p = float(sys.argv[2])
ratio = float(sys.argv[3])
method_id = int(sys.argv[4])

bots_num = int(percent_bot*node)  # number of the bots in the system

G_old = DirectedHighCluster_out(node, m, p).generate()

networkFile = './gmls/directedHighCluster_{}_{}_{}.gml'.format(node, m, p) # gml format network save file
if not os.path.exists(networkFile): # create, then save it for other percent_bot
   print 'Creating network, then save it...'
   G_old = DirectedHighCluster_out(node, m, p).generate()
   nx.write_gml(G_old, networkFile)
else:
   print 'Loading network...'
   G_old = nx.read_gml(networkFile)

rewire_method = rewire_method_proxy(method_id)
G_old_rewire = rewire_method(G_old, ratio)
if method_id == 7:
   nx.write_gml(G_old_rewire, './gmls/directedHighCluster_{}_{}_{}_{}_flip{}.gml'.format(node, m, p, ratio))
elif method_id == 2:
   nx.write_gml(G_old_rewire, './gmls/directedHighCluster_{}_{}_{}_rewire{}.gml'.format(node, m, p, method_id))
else:
   nx.write_gml(G_old_rewire, './gmls/directedHighCluster_{}_{}_{}_{}_rewire{}.gml'.format(node, m, p, ratio, method_id))

old_in =  G_old.in_degree()
old_rewire_in =  G_old_rewire.in_degree()
old_out =  G_old.out_degree()
old_rewire_out =  G_old_rewire.out_degree()

fp = open("result_{}_{}_{}.txt".format(p, ratio, method_id), "w")
print >> fp, "    \t\t in_degree \t\t out_degree"
print >> fp, "Node\t\tOld\tRewire\t\tOld\tRewire"
for n in G_old.nodes():
    print >> fp, "{}\t\t{}\t{}\t\t{}\t{}".format(n, old_in[n], old_rewire_in[n], old_out[n], old_rewire_out[n])
fp.close()

cnt = Counter(old_in.values())
xs, ys = cnt.keys(), cnt.values()
ys = np.array(ys)*1.0 / np.sum(ys)
plt.loglog(xs, ys, '*', label='old')

cnt = Counter(old_rewire_in.values())
xs, ys = cnt.keys(), cnt.values()
ys = np.array(ys)*1.0 / np.sum(ys)
plt.loglog(xs, ys, 'o', label='rewire')
plt.title('in-degree distribution')

plt.legend(loc='best')
plt.savefig('directedHCOut_indegree_distr_{}_{}_{}.png'.format(p, ratio, method_id))
plt.close()
