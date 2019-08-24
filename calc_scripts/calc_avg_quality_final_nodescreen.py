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

normal       = True if sys.argv[11] == 'normal' else False
nozero       = True if sys.argv[12] == 'nozero' else False
data_dir     = sys.argv[13]
save_dir     = sys.argv[14]
#========= END PARAMETERS =========

nodescreen_times = data_dir+'/{}/final_quality_nodescreen_{}_{}_{}_{}_{}_{}_{}_{}.pkl'
avg_quality_datas_dict = {}
normal_node = n
for h in phis:
    for w in wires:
        avg_qualities_temp = []
        for iter_ in range(run_times):
            fname = nodescreen_times.format(iter_, n, m, p, percent_bots, w, h, alpha, mu)
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
