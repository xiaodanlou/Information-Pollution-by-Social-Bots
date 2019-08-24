#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: rosdays

@description: plot human/bot meme posts distribution
"""

from __future__ import division
import matplotlib as mpl
mpl.use('Agg')

import os
import sys
import numpy as np
import cPickle as pickle
import matplotlib.pyplot as plt


#========== PARAMETERS ==========
wires    = map(float, sys.argv[1].split(','))
phis     = map(int, sys.argv[2].split(','))
data_dir = sys.argv[3]
save_dir = sys.argv[4]
#========= END PARAMETERS =========

fp = open(data_dir + '/bad_meme_selected_datas.pkl', 'rb')
bad_meme_select_data = pickle.load(fp)
fp.close()

fig_name_template = save_dir + '/bad_meme_selected_distr_{}.png'
for h in phis:
    plt.figure(figsize=(10, 5))
    for w in wires:
        all_mids_heights_pairs = bad_meme_select_data[(h, w)]
        all_mids = []
        all_heights = []
        for pair in all_mids_heights_pairs:
            mids_, heights_ = zip(*pair)
            all_mids.append(mids_)
            all_heights.append(heights_)

        print all_mids
        max_len = max([len(mid_) for mid_ in all_mids])
        sum_mids = [[] for _ in range(max_len)]
        sum_heights =[[] for _ in range(max_len)]
        for mid_ in all_mids:
            for idx, mi in enumerate(mid_):
                sum_mids[idx].append(mi)
        for height_ in all_heights:
            for idx, he in enumerate(height_):
                sum_heights[idx].append(he)

        # avg
        mids = [np.mean(sm)for sm in sum_mids]
        heights = [np.mean(sh) for sh in sum_heights]
        ratios = [np.log(height_)/np.log(mid_) for height_, mid_ in zip(heights, mids)]

        plt.subplot(121)
        plt.loglog(mids, heights, marker='o', label='$\\gamma$:'+str(w))
        plt.subplot(122)
        plt.plot(mids, ratios, marker='o', label='$\\gamma$:'+str(w))
        plt.xscale('log')

    # save fig
    plt.subplot(121)
    plt.loglog([min(mids), max(mids)], [min(mids), max(mids)], '--')
    plt.xlabel("Bot posts per meme", fontsize=14)
    plt.ylabel("Human posts per meme", fontsize=14)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.margins(0.1)
    plt.legend(loc='best', fontsize=14)

    plt.subplot(122)
    plt.xlabel("Bot posts per meme", fontsize=14)
    plt.ylabel("Exponent $\\eta$", fontsize=14)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.margins(0.1)
    plt.legend(loc='best', fontsize=14)

    plt.subplots_adjust(left=0.1, bottom=0.14, wspace=0.4)
    plt.savefig(fig_name_template.format(h))
    plt.close()
