#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: rosdays

@description: calculate popularity distributions of low quality memes and high quality memes
"""

from __future__ import division
import os
import sys
import numpy as np
import cPickle as pickle

from collections import defaultdict


base = 1.5
def logbase(x):
    return np.log(x)/np.log(base)

def get_count(list):
    count = {}
    for i, q in enumerate(list):
        if q in count.keys():
            count[q]+=1
        else:
            count[q]=1
    return count

def get_distr(count):
    distr = {}
    sum = 0
    aver = 0
    for a in count.keys():
        sum += count[a]
        aver += a*count[a]
        bin = int(logbase(a))
        if bin in distr.keys():
            distr[bin] += count[a]
        else:
            distr[bin] = count[a]
    return distr, sum

def getbins(distr, sum):
    mids = []
    heights = []
    bin = sorted(distr.keys())
    for i in bin:
        start = base ** i
        width = base ** (i+1)-start
        mid = start + width/2
        mids.append(mid)
        heights.append(distr[i]/(sum * width))
    return mids, heights


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

data_dir     = sys.argv[10]
save_dir     = sys.argv[11]
#========= END PARAMETERS =========

qua_of_low_qua_meme = 0.0
data_template_times = data_dir + '/tracked_memes_quality_and_popularity_{}_{}_{}_{}_{}_{}_{}_{}.pkl'
low_high_datas_dict = {}
for h in phis:
    for w in wires:
        fname = data_template_times.format(n, m, p, percent_bots, w, h, alpha, mu)
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
        quality_new = quality_new + [0]*len(zero_memes_number_selected)
        number_selected_new = number_selected_new + zero_memes_number_selected

        low_quality_pop = []
        high_quality_pop = []
        for qua, pop in zip(quality_new, number_selected_new):
            if qua > qua_of_low_qua_meme:
                high_quality_pop.append(pop)
            else:
                low_quality_pop.append(pop)

        count = get_count(high_quality_pop)
        distr, sum_ = get_distr(count)
        h_mids, h_heights = getbins(distr, sum_)

        count = get_count(low_quality_pop)
        distr, sum_ = get_distr(count)
        l_mids, l_heights = getbins(distr, sum_)

        low_high_datas_dict[(h, w)] = [h_mids, h_heights, l_mids, l_heights]

fw = open(save_dir + '/low_high_datas_{}.pkl'.format(nth), 'wb')
pickle.dump(low_high_datas_dict, fw)
fw.close()
