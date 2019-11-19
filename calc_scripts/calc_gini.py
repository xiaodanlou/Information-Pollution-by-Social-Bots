#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import division
import os
import sys
import numpy as np
import networkx as nx
import cPickle as pickle


#========== PARAMETERS ==========
nth          = int(sys.argv[1]) # n-th model result

n            = int(sys.argv[2])
m            = int(sys.argv[3])
p            = float(sys.argv[4])

percent_bots = float(sys.argv[5])
wires        = map(float, sys.argv[6].split(','))
phis         = map(float, sys.argv[7].split(','))
alpha        = None if sys.argv[8] == 'none' else int(sys.argv[8])
mu           = None if sys.argv[9] == 'none' else float(sys.argv[9])
run_times    = int(sys.argv[10])

data_dir     = sys.argv[11]
save_dir     = sys.argv[12]
network_dir  = sys.argv[13]
#========= END PARAMETERS =========

nodescreen_times = data_dir+'/{}/final_quality_nodescreen_{}_{}_{}_{}_{}_{}_{}_{}.pkl'
network_file = network_dir+'/directedHighCluster_{}_{}_{}.gml'.format(n, m, p)
g = nx.read_gml(network_file)
node_degree_pairs = g.degree(g.nodes())
# 按照度（入度+出度）排序节点<稳定排序>
nodes, degrees = zip(*sorted(node_degree_pairs.items(), key=lambda x:x[1]))

gini_datas_dict = {}
xs = np.arange(0, 1.1, 0.1)

normal_node = n
for h in phis:
    for w in wires:
        gini_temp = []
        for iter_ in range(run_times):
            fname = nodescreen_times.format(iter_, n, m, p, percent_bots, w, h, alpha, mu)
            fp = open(fname)
            temp = pickle.load(fp)
            fp.close()
            temp = temp[:normal_node, :] # normal node quality nodescreen

            # calc_gini
            each_node_bad_memes_num = np.sum(temp==0, axis=1)
            whole_bad_memes_num = np.sum(each_node_bad_memes_num)
            node_bad_memes_sorted_idx = np.argsort(each_node_bad_memes_num)

            gini = []
            for x in xs:
                nodes_idx = node_bad_memes_sorted_idx[:int(n*x)] # cumulative
                temp_ = temp[nodes_idx, :]
                bad_memes_num = np.sum(temp_==0) # bad meme's quality=0.0
                bad_memes_ratio = (bad_memes_num*1.0) / whole_bad_memes_num
                gini.append(bad_memes_ratio)
            gini_temp.append(gini)
        gini_datas_dict[(h, w)] = np.mean(gini_temp, axis=0).tolist()

fw = open(save_dir + '/gini_datas_{}.pkl'.format(nth), 'wb')
pickle.dump(gini_datas_dict, fw)
fw.close()
