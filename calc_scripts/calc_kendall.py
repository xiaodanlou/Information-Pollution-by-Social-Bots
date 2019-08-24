#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: rosdays

@description: calculate kendall distribution data
"""

from __future__ import division
import os
import sys
import numpy as np
import cPickle as pickle

from scipy import stats
from collections import defaultdict


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
nozero       = True if sys.argv[10] == 'nozero' else False

data_dir     = sys.argv[11]
save_dir     = sys.argv[12]
#========= END PARAMETERS =========

kendall_data_template_times = data_dir + '/tracked_memes_quality_and_popularity_{}_{}_{}_{}_{}_{}_{}_{}.pkl'
kendall_datas_dict = {}
for h in phis:
    for w in wires:
        fname = kendall_data_template_times.format(n, m, p, percent_bots, w, h, alpha, mu)
        fp = open(fname, 'rb')
        data = pickle.load(fp)
        fp.close()
        quality, number_selected = zip(*data)

        zero_memes_number_selected = []
        q_p_dict = defaultdict(list)
        for qua, num in zip(quality, number_selected):
            if qua != 0:
                q_p_dict[qua].append(num)
            else:
                zero_memes_number_selected.append(num)

        quality_new = []
        number_selected_new = []
        for meme, selected_nums in q_p_dict.iteritems():
            quality_new.append(meme)
            number_selected_new.append(np.mean(selected_nums))
        if not nozero:
            quality_new = quality_new + [0]*len(zero_memes_number_selected)
            number_selected_new = number_selected_new + zero_memes_number_selected

        kendall_tau, _ = stats.kendalltau(quality_new, number_selected_new)
        kendall_datas_dict[(h, w)] = kendall_tau

if nozero:
    fw = open(save_dir + '/kendall_datas_no_zero_{}.pkl'.format(nth), 'wb')
    pickle.dump(kendall_datas_dict, fw)
    fw.close()
else:
    fw = open(save_dir + '/kendall_datas_zero_{}.pkl'.format(nth), 'wb')
    pickle.dump(kendall_datas_dict, fw)
    fw.close()
