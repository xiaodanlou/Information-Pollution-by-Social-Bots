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

def func_linear(x, a, b):
    return a*x+b

def func_non_linear(x, a, b, c):
    return a*(x**b)+c

n = 10000
m = 3
percent_bots = 0.1
mu = None
alpha = 15

#wires = [0.0, 0.0001, 0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1.0]
wires = [0.001, 0.005, 0.01, 0.05, 0.1, 0.3, 0.5, 0.8, 1.0]
#phis = [1.0, 5.0, 10.0]
phis = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]

p = sys.argv[1]
nth = sys.argv[2]
data_dir = sys.argv[3]
save_dir = sys.argv[4]

data_template_times = data_dir + '/bad_meme_selected_data_{}_{}_{}_{}_{}_{}_{}_{}.pkl'

bad_meme_select_datas_dict = {}

for h in phis:
    for w in wires:
        merge = {}
        fname = data_template_times.format(n, m, p, percent_bots, w, h, alpha, mu)
        fp = open(fname, 'rb')
        data = pickle.load(fp)
        fp.close()
        #fitness, good_selected, bad_selected = zip(*data)
        #good_selected = np.array(good_selected) + 1
        #bad_selected = np.array(bad_selected) + 1
        #print 'max good selected:', max(good_selected)
        #print 'max bad selected:', max(bad_selected)

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
