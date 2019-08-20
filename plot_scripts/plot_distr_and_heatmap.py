#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: rosdays

@description: plot kendall/avg_quality/diveristy distribution&heatmap
"""

from __future__ import division
import matplotlib as mpl
mpl.use('Agg')

import os
import sys
import numpy as np
import cPickle as pickle
import matplotlib.pyplot as plt


def draw_heatmap(ax, data, xticks, yticks, xlabel, ylabel, cmap, title, vmax=None, vmin=None):
    data = data[::-1, :]
    if vmin == None:
        vmin = data[0][0]
        for i in data:
            for j in i:
                if j<vmin:
                    vmin=j
    if vmax == None:
        vmax = data[0][0]
        for i in data:
            for j in i:
                if j>vmax:
                    vmax=j

    map = ax.imshow(data, interpolation='nearest', cmap=cmap, aspect='auto', vmin=vmin, vmax=vmax)
    yticks = yticks[::-1]
    ax.set_yticks(range(len(yticks)))
    ax.set_yticklabels(yticks, fontsize=14)
    ax.set_xticks(range(len(xticks)))
    ax.set_xticklabels(xticks, fontsize=14)#, rotation=40
    cb = plt.colorbar(mappable=map, cax=None, ax=None)
    cb.ax.tick_params(labelsize=12)
    plt.xlabel(xlabel, fontsize=14)
    plt.ylabel(ylabel, fontsize=14)
    plt.title(title)


data_dir = sys.argv[1]
save_dir = sys.argv[2]

# data options
wires = [0.001, 0.005, 0.01, 0.05, 0.1, 0.3, 0.5, 0.8, 1.0]
new_wires = wires
phis1  = [1.0, 5.0, 10.0]
phis2  = phis1

# plot options
xs = phis2
ys = wires
cmap = None
xlabel = '$\\phi$'
ylabel = '$\\gamma$'

kendall_pic_title = 'Discriminative power'
avg_quality_pic_title = 'Average Quality'
diversity_pic_title = 'Diversity'

figure = plt.figure(figsize=(13, 15), facecolor='w')
markers = ["o", "s", "^"]

### 1. average quality (final nodescreen) ###
avg_quality_data = []
fp = open(data_dir + '/avg_quality_datas_zero.pkl', 'rb')

avg_quality_data = pickle.load(fp)
fp.close()
grid = np.zeros((len(wires), len(phis2)))
for i, w in enumerate(wires):
    for j, h in enumerate(phis2):
            grid[i, j] = np.mean(avg_quality_data[(h, w)])

# distr plot
ax = figure.add_subplot(3,2,1)
for idx, h in enumerate(phis1):
    avg_qualities = []
    stds = []
    for w in wires:
        avg_qualities.append(np.mean(avg_quality_data[(h, w)]))
        stds.append(np.std(avg_quality_data[(h, w)]))
    ax.plot(new_wires, avg_qualities, marker=markers[idx], label='$\\phi$:'+str(h))

ax.set_xlabel('$\\gamma$', fontsize=14)
ax.set_ylabel('Average quality', fontsize=14)
ax.set_xscale('log')
ax.set_xlim((new_wires[0], new_wires[-1]))
ax.set_xlim((new_wires[0], new_wires[-1]))
ax.legend(loc='upper right', fontsize=14)

# heatmap plot
ax = figure.add_subplot(3,2,2)
draw_heatmap(ax, grid, xs, ys, xlabel, ylabel, cmap, avg_quality_pic_title, vmin=None, vmax=None)


### 2. diversity (final nodescreen) ###
diversity_data = []
fp = open(data_dir + '/diversity_datas_no_zero.pkl', 'rb')
diversity_data = pickle.load(fp)
fp.close()

# distr plot
ax = figure.add_subplot(3,2,3)
for idx, h in enumerate(phis1):
    diversities = []
    stds = []
    for w in wires:
        diversities.append(np.mean(diversity_data[(h, w)]))
        stds.append(np.std(diversity_data[(h, w)]))
    ax.plot(new_wires, diversities, marker=markers[idx], label='$\\phi$:'+str(h))

ax.set_xlabel('$\\gamma$', fontsize=14)
ax.set_ylabel('Diversity', fontsize=14)
ax.set_xscale('log')
ax.set_xlim((new_wires[0], new_wires[-1]))
ax.set_xlim((new_wires[0], new_wires[-1]))

# heatmap plot
ax = figure.add_subplot(3,2,4)
grid = np.zeros((len(wires), len(phis2)))
for i, w in enumerate(wires):
    for j, h in enumerate(phis2):
            grid[i, j] = np.mean(diversity_data[(h, w)])

draw_heatmap(ax, grid, xs, ys, xlabel, ylabel, cmap, diversity_pic_title, vmin=None, vmax=None)


### 3. kendall ###
kendall_data = []
fp = open(data_dir + '/kendall_datas_no_zero.pkl', 'rb')
kendall_data = pickle.load(fp)
fp.close()

# distr plot
ax = figure.add_subplot(3,2,5)
for idx, h in enumerate(phis1):
    kendalls = []
    stds = []
    for w in wires:
        kendalls.append(np.mean(kendall_data[(h, w)]))
        stds.append(np.std(kendall_data[(h, w)]))
    ax.plot(new_wires, kendalls, marker=markers[idx], label='$\\phi$:'+str(h))

ax.set_xlabel('$\\gamma$', fontsize=14)
ax.set_ylabel('Discriminative power', fontsize=14)
ax.set_xscale('log')
ax.set_xlim((new_wires[0], new_wires[-1]))
ax.set_xlim((new_wires[0], new_wires[-1]))
# ax.legend(loc='lower left', fontsize=14)

# heatmap plot
ax = figure.add_subplot(3,2,6)
grid = np.zeros((len(wires), len(phis2)))
for i, w in enumerate(wires):
    for j, h in enumerate(phis2):
            grid[i, j] = np.mean(kendall_data[(h, w)])
draw_heatmap(ax, grid, xs, ys, xlabel, ylabel, cmap, kendall_pic_title, vmin=None, vmax=None)


### 4. save plot ###
plt.subplots_adjust(left=0.1, right=0.95, top=0.95, bottom=0.05, wspace=0.3, hspace=0.3)
plt.savefig(save_dir + "/all_distr_heatmap.png")
