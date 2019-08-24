#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import division
import matplotlib as mpl
mpl.use('Agg')

import os
import sys
import numpy as np
import pandas as pd
import cPickle as pickle
import matplotlib.pyplot as plt


#========== PARAMETERS ==========
wires    = map(float, sys.argv[1].split(','))
phis     = map(int, sys.argv[2].split(','))
nozero   = True if sys.argv[3] == 'nozero' else False
data_dir = sys.argv[4]
save_dir = sys.argv[5]
#========= END PARAMETERS =========

new_wires = wires
models = ['random', 'prefer']
if nozero:
    avg_quality_data_file_template = data_dir + '/avg_quality_datas_no_zero.pkl'
else:
    avg_quality_data_file_template = data_dir + '/avg_quality_datas_zero.pkl'

model_data = {}
for model in models:

    data_path = avg_quality_data_file_template
    fp = open(data_path, 'rb')
    avg_quality_data = pickle.load(fp)
    fp.close()

    all_avg_quality_data = []
    all_avg_quality_mean_data = []
    for h in phis:
        avg_qualities = []
        avg_qualities_mean = []

        for w in wires:
            print len(avg_quality_data[(h, w)])
            avg_qualities.append(avg_quality_data[(h, w)])
            avg_qualities_mean.append(np.mean(avg_quality_data[(h, w)]))

        all_avg_quality_data.append(avg_qualities)
        all_avg_quality_mean_data.append(avg_qualities_mean)

    model_data[model] = [all_avg_quality_data, all_avg_quality_mean_data]

# compute `prefer_attach/random_choice` relatives
relatives_bound_all = []
markers = ["o", "s", "^"]
for ih, h in enumerate(phis):
    relatives = []
    relatives_low = []
    relatives_up = []
    #colors = ['b','r','y']
    for iw, w in enumerate(wires):
        alls1, means1 = model_data['prefer']
        alls2, means2 = model_data['random']
        relatives.append(means1[ih][iw]/means2[ih][iw])

        temp = []
        for d1, d2 in zip(alls1[ih][iw], alls2[ih][iw]):
            rel = d1 / d2
            temp.append(rel)
        n = len(temp)
        std = np.std(temp)
        mean = np.mean(temp)
        relatives_low.append(mean-1.96*std/np.sqrt(n))
        relatives_up.append(mean+1.96*std/np.sqrt(n))

    plt.plot(new_wires, relatives, marker=markers[ih], label='$\\phi$:'+str(h)) #color=colors[ih]
    plt.fill_between(new_wires, relatives_low, relatives_up, alpha=0.4) #color=colors[ih]


plt.plot([min(new_wires), max(new_wires)], [1, 1], '--')
# plt.axvspan(0.4, 0.6, facecolor='#2ca02c', alpha=0.2)

plt.xlabel('$\\gamma$', fontsize=14)
plt.ylabel('Relative average quality', fontsize=14)
plt.xscale('log')

plt.xlim((new_wires[0], new_wires[-1]))
#locs, labels = plt.xticks()
#plt.xticks(locs, [0]+['$\\mathdefault{0}$', '$\\mathdefault{10^{-4}}$', '$\\mathdefault{10^{-3}}$', '$\\mathdefault{10^{-2}}$', '$\\mathdefault{10^{-1}}$', '$\\mathdefault{10^{0}}$']+[0])
plt.xlim((new_wires[0], new_wires[-1]))

plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.legend(loc='upper left', fontsize=14)
plt.subplots_adjust(bottom=0.14)
if nozero:
    plt.savefig(save_dir + '/avg_quality_fitness_relative_no_zero.png')
else:
    plt.savefig(save_dir + '/avg_quality_fitness_relative.png')
