#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
@author: rosdays

@description: calculate average quality distribution data
"""

from __future__ import division
import os
import sys
import numpy as np
import cPickle as pickle


wires = [0.001, 0.005, 0.01, 0.05, 0.1, 0.3, 0.5, 0.8, 1.0]
phis = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]

node = 10000
m = 3
percent_bots = 0.1
mu = None
alpha = 15
run_times = 1

p = sys.argv[1]
nth = sys.argv[2] # n-th model result
normal = True if sys.argv[3] == 'normal' else False
nozero = True if sys.argv[4] == 'nozero' else False
data_dir = sys.argv[5]
save_dir = sys.argv[6]

nodescreen_times = data_dir+'/{}/final_quality_nodescreen_{}_{}_{}_{}_{}_{}_{}_{}.pkl'

avg_quality_datas_dict = {}

normal_node = node
for h in phis:
    for w in wires:
        avg_qualities_temp = []
        for iter_ in range(run_times):
            fname = nodescreen_times.format(iter_, node, m, p, percent_bots, w, h, alpha, mu)
            fp = open(fname)
            temp = pickle.load(fp)
            fp.close()
            if normal:
                temp = temp[:normal_node, :]
            if nozero:
                temp = temp[temp!=0]
            avg_quality_meme = np.mean(temp)
            avg_qualities_temp.append(avg_quality_meme)
        avg_quality_datas_dict[(h, w)] = np.mean(avg_qualities_temp)

if nozero:
    fw = open(save_dir + '/avg_quality_datas_no_zero_{}.pkl'.format(nth), 'wb')
    pickle.dump(avg_quality_datas_dict, fw)
    fw.close()
else:
    fw = open(save_dir + '/avg_quality_datas_zero_{}.pkl'.format(nth), 'wb')
    pickle.dump(avg_quality_datas_dict, fw)
    fw.close()
