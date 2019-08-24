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
coupled_gml_dir = sys.argv[13]
#========= END PARAMETERS =========

nodescreen_times = data_dir+'/{}/final_quality_nodescreen_{}_{}_{}_{}_{}_{}_{}_{}.pkl'
coupled_gml = 'directedHighCluster_{}_{}_{}_{}_{}_{}_{}_{}_coupled.gml'

normal_node = n
for h in phis:
    for w in wires:
        quality_temp = []
        bad_meme_num_temp = []
        for iter_ in range(run_times):
            fname = nodescreen_times.format(iter_, n, m, p, percent_bots, w, h, alpha, mu)
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
        fname = coupled_gml.format(n, m, p, percent_bots, w, int(h), alpha, str(mu).lower())
        g = nx.read_gml(os.path.join(coupled_gml_dir, fname))
        for node_ in g.nodes():
            isbot = 0 if int(node_) <= normal_node else 1
            bad_num = avg_bad_meme_num[int(node_)]
            avg_qua = avg_quality[int(node_)]
            g.node[node_]['bot'] = isbot
            g.node[node_]['badnum'] = bad_num
            g.node[node_]['avgqua'] = avg_qua

        nx.write_gml(g, save_dir + '/' + fname[:-4]+'.gml')
