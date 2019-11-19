#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: rosdays

@description: plot low&high quality distribution
"""

from __future__ import division
import matplotlib as mpl
mpl.use('Agg')

import os
import sys
import numpy as np
import cPickle as pickle
import matplotlib.pyplot as plt

from itertools import chain
from collections import defaultdict


#========== PARAMETERS ==========
wires    = map(float, sys.argv[1].split(','))
phis     = map(int, sys.argv[2].split(','))
data_dir = sys.argv[3]
save_dir = sys.argv[4]
#========= END PARAMETERS =========

low_high_data = []
fp = open(data_dir + '/low_high_datas.pkl', 'rb')
low_high_data = pickle.load(fp)
fp.close()

fig, axs = plt.subplots(len(phis), len(wires), figsize=(14, 8))
for i, h in enumerate(phis):
    for j, w in enumerate(wires):
        if len(zip(*low_high_data[(h, w)])) < 4: # data invalid!!!
            continue
        h_mids_, h_heights_, l_mids_, l_heights_ = zip(*low_high_data[(h, w)])

        h_mids_all = chain.from_iterable(h_mids_) # flat list of list
        h_heights_all = chain.from_iterable(h_heights_) # flat list of list
        l_mids_all = chain.from_iterable(l_mids_) # flat list of list
        l_heights_all = chain.from_iterable(l_heights_) # flat list of list

        h_dict = defaultdict(list)
        for hm, hh in zip(h_mids_all, h_heights_all):
            h_dict[hm].append(hh)
        l_dict = defaultdict(list)
        for lm, lh in zip(l_mids_all, l_heights_all):
            l_dict[lm].append(lh)

        hs = []
        for k, v in h_dict.iteritems():
            hs.append([k, np.mean(v)])
        if len(hs) == 0:
            print >> sys.stderr, "something wrong!"
            sys.exit(1)
        h_mids, h_heights = zip(*sorted(hs, key=lambda x:x[0]))
        ls = []
        for k, v in l_dict.iteritems():
            ls.append([k, np.mean(v)])
        if len(ls) == 0:
            print >> sys.stderr, "something wrong!"
            sys.exit(1)
        l_mids, l_heights = zip(*sorted(ls, key=lambda x:x[0]))

        ax = axs[i][j]
        ax.loglog(h_mids, h_heights, marker='s', label='high quality')
        ax.loglog(l_mids, l_heights, marker='^', label='low quality')
        ax.set_xlabel('popularity', fontsize=14)
        ax.set_ylabel('P(popularity)', fontsize=14)
        ax.tick_params(labelsize=14)
        ax.annotate('$\\gamma={}$\n$\\phi={}$'.format(w, h), xy=(0.05, 0.05), xycoords='axes fraction', fontsize=12)
        if i == 0 and j == 0:
            ax.legend(loc="upper right", fontsize=15)

plt.subplots_adjust(left=0.08, right=0.92, top=0.92, wspace=0.3, hspace=0.3)
plt.savefig(save_dir + '/meme_quality_distr.png')
plt.close()
