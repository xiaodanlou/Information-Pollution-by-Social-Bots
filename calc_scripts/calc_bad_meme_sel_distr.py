#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
@author: rosdays

@description: calculate meme posts distribution data
"""

from __future__ import division
import os
import sys
import numpy as np
import cPickle as pickle


base = 1.5
def logbase(x):
    return np.log(x)/np.log(base)

def get_distr(count):
    distr_x = {}
    distr_y = {}
    for a in count.keys():
        bin = int(logbase(a))

        # x
        if bin in distr_x.keys():
            distr_x[bin].append(a)
        else:
            distr_x[bin] = []
            distr_x[bin].append(a)

        # y
        if bin in distr_y.keys():
            distr_y[bin].append(count[a])
        else:
            distr_y[bin] = []
            distr_y[bin].append(count[a])
    return distr_x, distr_y

def getbins(distr_x, distr_y):
    mids = []
    heights = []
    bin = sorted(distr_x.keys())
    for i in bin:
        #start = base ** i
        #width = base ** (i+1)-start
        #mid = start + width/2
        mids.append(np.mean(distr_x[i]))
        heights.append(np.mean(distr_y[i]))
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

data_template_times = data_dir + '/bad_meme_selected_data_{}_{}_{}_{}_{}_{}_{}_{}.pkl'
bad_meme_select_datas_dict = {}
for h in phis:
    for w in wires:
        merge = {}
        fname = data_template_times.format(n, m, p, percent_bots, w, h, alpha, mu)
        fp = open(fname, 'rb')
        data = pickle.load(fp)
        fp.close()

        for idx in xrange(len(data)):
            fit  = data[idx][0]
            good = data[idx][1] + 1
            bad  = data[idx][2] + 1
            if fit not in merge:
                merge[fit] = [[], []]
            merge[fit][0].append(good)
            merge[fit][1].append(bad)

        good_selected = []
        bad_selected = []
        for _, value in merge.iteritems():
            good_selected.append(np.mean(value[0]))
            bad_selected.append(np.mean(value[1]))
        count = dict([val for val in zip(bad_selected, good_selected)])
        distr_x, distr_y = get_distr(count)
        mids, heights = getbins(distr_x, distr_y)

        bad_meme_select_datas_dict[(h, w)] = zip(mids, heights)

fw = open(save_dir + '/bad_meme_selected_datas_{}.pkl'.format(nth), 'wb')
pickle.dump(bad_meme_select_datas_dict, fw)
fw.close()
