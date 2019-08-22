#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
@author: rosdays

@description: calculate coupled gmls
"""

from __future__ import division
import os
import sys
import numpy as np
import networkx as nx
import cPickle as pickle


wires = [0.1]
phis = [5.0]

node = 1000
m = 3
percent_bots = 0.1
mu = None
alpha = 15
run_times = 3

p = sys.argv[1]
nth = sys.argv[2] # n-th model result
rewire2 = sys.argv[3] # 0/1
data_dir = sys.argv[4]
save_dir = sys.argv[5]
coupled_gml_dir = sys.argv[6]


nodescreen_times = data_dir+'/{}/final_quality_nodescreen_{}_{}_{}_{}_{}_{}_{}_{}.pkl'
coupled_gmls = ['directedHighCluster_{}_{}_{}_{}_{}_{}_{}_{}_coupled.gml',
                'directedHighCluster_{}_{}_{}_{}_{}_{}_{}_{}_coupled_rewire2.gml']


for coupled_gml in coupled_gmls:
    normal_node = node
    for h in phis:
        for w in wires:
            quality_temp = []
            bad_meme_num_temp = []
            for iter_ in range(run_times):
                fname = nodescreen_times.format(iter_, node, m, p, percent_bots, w, h, alpha, mu)
                fp = open(fname)
                temp = pickle.load(fp)
                fp.close()
                quality = np.mean(temp, axis=1).tolist()
                bad_meme_num = np.sum(temp == 0, axis=1).tolist()
                quality_temp.append(quality)
                bad_meme_num_temp.append(bad_meme_num)
            avg_quality = np.mean(quality_temp, axis=0).tolist()
            avg_bad_meme_num = np.mean(bad_meme_num_temp, axis=0).tolist()

            # add attribute to network
            fname = coupled_gml.format(node, m, p, percent_bots, w, int(h), alpha, str(mu).lower())
            g = nx.read_gml(os.path.join(coupled_gml_dir, fname))
            for node_ in g.nodes():
                isbot = 0 if int(node_) <= normal_node else 1
                bad_num = avg_bad_meme_num[int(node_)]
                avg_qua = avg_quality[int(node_)]
                g.node[node_]['bot'] = isbot
                g.node[node_]['bad_num'] = bad_num
                g.node[node_]['avg_qua'] = avg_qua

            nx.write_gml(g, save_dir + '/' + fname[:-4]+'.gml')
