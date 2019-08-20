#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: rosdays

@description: push model, different network structure,
              bots create different low quality memes (with different fitness).
"""

from __future__ import division
import matplotlib as mpl
mpl.use('Agg')

import os
import sys
import time
import random
import numpy as np
import networkx as nx
import cPickle as pickle
import matplotlib.pyplot as plt

from scipy import stats
from collections import defaultdict
from itertools import count as infinite_iter

if sys.version_info.major != 2 or sys.version_info.minor != 7:
    raise EnvironmentError, "`python` version should be 2.17.x"

if nx.__version__ != "1.11":
    raise ImportError, "`networkx` version should be 1.11"

class DirectedHighCluster_out(object):
    def __init__(self, n, m=3, p=0.5):
        self.n = n
        self.m = m
        self.p = p
        self.G = nx.DiGraph()

    def generate(self):
        self.G.add_edges_from([(0,1),(0,2),(0,3),(1,0),(1,2),(1,3),(2,0),(2,1),(2,3),(3,1),(3,2),(3,0)])
        source = self.m + 1 # original 4 points
        while source < self.n:
            target = random.choice(self.G.nodes())
            self.G.add_edge(source, target)
            rest = 1
            while rest < self.m:
               # trial
                temp = random.random()
                if temp <= self.p:
                    neighbors = self.G.neighbors(target) # only out-degree neighbors ( same as self.G.successors(target) )
                    filte_neighbors = [nei for nei in neighbors if not self.G.has_edge(source, nei)]
                    if len(filte_neighbors) > 0:
                        target_nei = random.choice(filte_neighbors)
                        self.G.add_edge(source, target_nei)
                        rest += 1
                else:
                    # attach
                    current_nodes = [node for node in self.G.nodes() if source != node]
                    target_nodes = [c_node for c_node in current_nodes if not self.G.has_edge(source, c_node)]
                    if len(target_nodes) > 0:
                        target = random.choice(target_nodes)
                        self.G.add_edge(source, target)
                        rest += 1

            source += 1

        return self.G

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

def create_injection_network_random(G_normal, normal_n, bots_n, m, p, re_p):
    if bots_n == 0:
        return G_normal
    elif 0 < bots_n <=3:
        g = nx.DiGraph()
        G_bots = nx.cycle_graph(bots_n, create_using=g)
    else:
        G_bots = DirectedHighCluster_out(bots_n, m, p).generate()
    G_bots = nx.convert_node_labels_to_integers(G_bots, first_label=normal_n)

    G_whole = nx.compose(G_normal, G_bots)
    for i in G_bots.nodes():
        for j in G_normal.nodes():
            temp_p = random.uniform(0, 1)
            if temp_p <= re_p:
                G_whole.add_edge(j, i) # add directed link from `normal` to `bot`

    return G_whole

def choose_normal(nodes, nodes_p, nums):
    choose_nodes = []
    for i in range(nums):
        if (np.array(nodes_p) == 0).all():
            idx = random.randint(0, len(nodes_p)-1)
            choose_nodes.append(nodes[idx])
        else:
            prob = random.random()
            temp = np.cumsum(nodes_p) / np.sum(nodes_p)
            idx = np.where(temp >= prob)[0][0]
            choose_nodes.append(nodes[idx])
        del nodes[idx]
        del nodes_p[idx]
    return choose_nodes

def create_injection_network_prefer(G_normal, normal_n, bots_n, m, p, re_p):
    if bots_n == 0:
        return G_normal
    elif 0 < bots_n <=3:
        g = nx.DiGraph()
        G_bots = nx.cycle_graph(bots_n, create_using=g)
    else:
        G_bots = DirectedHighCluster_out(bots_n, m, p).generate()
    G_bots = nx.convert_node_labels_to_integers(G_bots, first_label=normal_n)
    number_connect = int(normal_n * re_p)

    G_whole = nx.compose(G_normal, G_bots)

    for i in G_bots.nodes():
        nodes = G_normal.nodes()
        nodes_p = [G_normal.in_degree(i_) for i_ in G_normal.nodes()]
        connect_normal = choose_normal(nodes, nodes_p, number_connect)
        for j in connect_normal:
            G_whole.add_edge(j, i) # add directed link from `normal` to `bot`

def inverseCdf(x, phi):
    return 1 - x**(1/(phi+1))

def myITMRandom(phi):
    x = random.uniform(0, 1)
    return inverseCdf(x, phi)

def myITMRandomArr(phi, size):
    zz = np.zeros(size)
    for row in range(size[0]):
        for col in range(size[1]):
            zz[row, col] = myITMRandom(phi)
    return zz


#========== main ==========

#========== PARAMETERS ==========
n = int(sys.argv[1]) # nodes
m = int(sys.argv[2])
p = float(sys.argv[3])

percent_bots = float(sys.argv[4]) # percent of bots
wire         = float(sys.argv[5])
phi          = float(sys.argv[6]) # the fitness
alpha        = None if sys.argv[7] == 'none' else int(sys.argv[7])
mu           = None if sys.argv[8] == 'none' else float(sys.argv[8]) # probability to choose existing meme, if None, then from empirical distribution

networkFile     = sys.argv[9]
coupled_gml     = sys.argv[10]
results_save_to = sys.argv[11]
mode            = sys.argv[12] # random/prefer

bots_num            = int(percent_bots*n)  # number of the bots in the system
qua_of_low_qua_meme = 0
screen_size         = 15
track_memes_after   = 10**4 # only save memes after this step
max_memes_track     = 10**5 # number of memes to track after track_memes_after
times               = 3 # simulation times afer steady

muDisFile    = './twitter_mu_distribution.dat'
alphaDisFile = './2016_apv_distr_integer.txt'


#================================
print "******** PARAMS *********"
print 'Network: BA: n:{0}, m:{1}, bot:{2} screen:{3}'.format(n, m, bots_num, screen_size)
print 'wire: {} phi: {}'.format(wire, phi)
print 'alpha: {0} mu: {1} '.format(alpha, mu)
print 'Track memes after {0} steps'.format(track_memes_after)
print 'Max memes to track: {0}'.format(max_memes_track)
print "*************************"


print 'Init mu&alpha empirical distribution data...'
alphas_ = []
counts_ = []
with open(alphaDisFile) as fp:
    for line in fp:
        alpha_, count_ = map(int, line.rstrip().split())
        alphas_.append(alpha_)
        counts_.append(count_)

alpha_probs_ = np.array(counts_) / sum(counts_)
alpha_dis = (alphas_, alpha_probs_.tolist())

mus_ = []
mu_probs_ = []
with open(muDisFile) as fp:
    for line in fp:
        mu_, prob_ = map(float, line.rstrip().split())
        mus_.append(mu_)
        mu_probs_.append(prob_)
mu_dis = (mus_, mu_probs_)
if mu:
    mus = [mu] * (n+bots_num)
else:
    mus = np.random.choice(mu_dis[0], n+bots_num, p=mu_dis[1])


starttime = time.time()
print 'Loading network...'
G_old = nx.read_gml(networkFile)

if mode == "random":
    print "random choice mode: ", mode
    G = create_injection_network_random(G_old, n, bots_num, m, p, wire)
elif mode == "prefer":
    print "preferential attachment mode: ", mode
    G = create_injection_network_prefer(G_old, n, bots_num, m, p, wire)
else:
    print "error, not support mode: ", mode
    sys.exit(1)

nx.write_gml(G, coupled_gml)
adj = dict([(n_, G.predecessors(n_)) for n_ in G.nodes()])


print 'Init nodescreen...'
quality_nodescreen = myITMRandomArr(phi, (n+bots_num, screen_size))
quality_nodescreen[n:, :] = 0

fitness_nodescreen = quality_nodescreen.copy()
fitness_nodescreen[n:, :] = myITMRandomArr(1/phi, (bots_num, screen_size))


### get steady simulation ###
t1 = time.time()

print "Please wait while the simulation completes.."
bad_memes_select_nums = defaultdict(lambda :[0, 0])
normal_node_bad_memes_select_nums = defaultdict(lambda :[0, 0]) # {'node_id':[steady, steady2final], ...}

unique_meme_nums                  = []
each_step_select_node             = []
each_step_bad_memes_nums          = []
each_step_nodes_contain_bad_memes = []
each_step_normal_nodes_avg_quality_steady = []

for counter in xrange(1, track_memes_after + 1):

    if counter % 1000:
        unique_meme_nums.append(len(np.unique(quality_nodescreen)))

    select_one_node = random.randint(0, n+bots_num-1) # [0, n+bots_num-1]
    probability_new_idea = random.uniform(0, 1) # mu, [0, 1)/ [0, 1] depending on rounding
    affectednodes = adj[select_one_node]
    if probability_new_idea <= mus[select_one_node]:
        ### create a new meme ###
        if select_one_node >= n:
            quality_chosen = 0
            fitness_chosen = myITMRandom(1/phi)
        else:
            quality_chosen = fitness_chosen = myITMRandom(phi) # quality&fitness for the new meme
    else:
        ### select a meme from self's screen ###
        my_alpha = np.random.choice(alpha_dis[0], p=alpha_dis[1]) # default only sample one element
        if alpha:
            my_alpha = alpha
        if my_alpha > screen_size:
            my_alpha = screen_size

        can_see_memes_quality = quality_nodescreen[select_one_node, :my_alpha]
        can_see_memes_fitness = fitness_nodescreen[select_one_node, :my_alpha]

        meme_probability = random.uniform(0, 1)
        temp = np.cumsum(can_see_memes_fitness.astype(np.float64)) / np.sum(can_see_memes_fitness.astype(np.float64))
        meme_idx = np.where(temp >= meme_probability)[0][0]
        quality_chosen = can_see_memes_quality[meme_idx] # selected meme
        fitness_chosen = can_see_memes_fitness[meme_idx]


    # diffuse meme's quality
    temp_quality = quality_nodescreen[affectednodes, :screen_size-1].copy()
    quality_nodescreen[affectednodes, 0] = quality_chosen
    quality_nodescreen[affectednodes, 1:] = temp_quality

    # diffuse meme's fitness
    temp_fitness = fitness_nodescreen[affectednodes, :screen_size-1].copy()
    fitness_nodescreen[affectednodes, 0] = fitness_chosen
    fitness_nodescreen[affectednodes, 1:] = temp_fitness

    # record something
    if quality_chosen == 0:
        if select_one_node < n:
            normal_node_bad_memes_select_nums[select_one_node][0] += 1
            bad_memes_select_nums[(quality_chosen, fitness_chosen)][0] += 1
        else:
            bad_memes_select_nums[(quality_chosen, fitness_chosen)][1] += 1

    each_step_nodes_contain_bad_memes.append(np.sum(np.sum(quality_nodescreen[:n, :]==0, axis=1)>=1))
    each_step_bad_memes_nums.append(np.sum(quality_nodescreen[:n, :]==0))
    each_step_select_node.append(select_one_node)
    each_step_normal_nodes_avg_quality_steady.append(np.mean(quality_nodescreen[:n, :]))

steady_quality_nodescreen = quality_nodescreen.copy()
steady_fitness_nodescreen = fitness_nodescreen.copy()

fp = open(results_save_to + '/steady_quality_nodescreen_{}_{}_{}_{}_{}_{}_{}_{}.pkl'.format(n, m, p, percent_bots, wire, phi, alpha, mu), 'wb')
pickle.dump(steady_quality_nodescreen, fp)
fp.close()

fp = open(results_save_to + '/steady_fitness_nodescreen_{}_{}_{}_{}_{}_{}_{}_{}.pkl'.format(n, m, p, percent_bots, wire, phi, alpha, mu), 'wb')
pickle.dump(steady_fitness_nodescreen, fp)
fp.close()

fp = open(results_save_to + '/each_step_normal_nodes_avg_quality_steady_{}_{}_{}_{}_{}_{}_{}_{}.pkl'.format(n, m, p, percent_bots, wire, phi, alpha, mu), 'wb')
pickle.dump(each_step_normal_nodes_avg_quality_steady, fp)
fp.close()

plt.figure(1)
plt.loglog(range(1, len(unique_meme_nums)+1), unique_meme_nums, 'r*')
plt.xlabel('step')
plt.ylabel('unique meme nums')
plt.savefig(results_save_to + '/unique_memes_{}_{}_{}_{}_{}_{}_{}_{}.png'.format(n, m, p, percent_bots, wire, phi, alpha, mu))
plt.close()

endtime = time.time()
print "Steady simulation ready! Total time in seconds: {}".format((endtime - t1))


### begin simulation ###
memes_all = [] # save each simulation's memes
bad_memes_select_nums_all = []
bad_meme_propagation_path_all = []
#each_step_normal_nodes_avg_quality_steady2final = defaultdict(list)
bad_memes_select_nums_all.append(bad_memes_select_nums)

print "Please wait while {} times simulations completes..".format(times)
max_meme_size = 0
for iter_ in range(times):
    meme_count = 0
    meme_dead = 0

    print "{}-th simulations start...".format(iter_+1)
    t1 = time.time()
    quality_nodescreen = steady_quality_nodescreen.copy()
    fitness_nodescreen = steady_fitness_nodescreen.copy()
    memes = {}
    bad_memes_select_nums = defaultdict(lambda :[0, 0])
    bad_meme_propagation_path = {}

    for counter in infinite_iter(track_memes_after):
        if counter % 1000 == 0:
            print "{}-th Simulation, step {}, {} memes borned. Elapsed time: {}".format(iter_+1, counter, meme_count, time.time()-t1)
            print "{}-th Simulation, step {}, {} memes deaded. Elapsed time: {}".format(iter_+1, counter, meme_dead, time.time()-t1)

        select_one_node = random.randint(0, n+bots_num-1)
        affectednodes = adj[select_one_node]
        affectednodes_normal = [an for an in affectednodes if an < n]
        probability_new_idea = random.uniform(0, 1) # mu
        if probability_new_idea <= mus[select_one_node]:
            ###create a new meme ###
            if select_one_node >= n:
                quality_chosen = 0
                fitness_chosen = myITMRandom(1/phi)
            else:
                quality_chosen = fitness_chosen = myITMRandom(phi) # fitness for the new meme

            if select_one_node >= n and quality_chosen == 0:
                if (quality_chosen, fitness_chosen) not in bad_meme_propagation_path:
                    bad_meme_propagation_path[(quality_chosen, fitness_chosen)] = [[select_one_node, affectednodes_normal]] # {(qua, fit):[[select_one_node, []],...]}
        else:
            ### select a meme from self's screen ###
            my_alpha = np.random.choice(alpha_dis[0], p=alpha_dis[1]) # default only sample one element
            if alpha:
                my_alpha = alpha
            if my_alpha > screen_size:
                my_alpha = screen_size

            neighbors = adj[select_one_node]
            can_see_memes_quality = quality_nodescreen[select_one_node, :my_alpha]
            can_see_memes_fitness = fitness_nodescreen[select_one_node, :my_alpha]

            meme_probability = random.uniform(0, 1)
            temp = np.cumsum(can_see_memes_fitness.astype(np.float64)) / np.sum(can_see_memes_fitness.astype(np.float64))
            meme_idx = np.where(temp >= meme_probability)[0][0]
            quality_chosen = can_see_memes_quality[meme_idx] # selected meme
            fitness_chosen = can_see_memes_fitness[meme_idx]

            if select_one_node < n and quality_chosen == 0:
                if (quality_chosen, fitness_chosen) in bad_meme_propagation_path:
                    bad_meme_propagation_path[(quality_chosen, fitness_chosen)].append([select_one_node, affectednodes_normal])

        if quality_chosen == 0:
            if select_one_node < n:
                normal_node_bad_memes_select_nums[select_one_node][1] += 1
                bad_memes_select_nums[(quality_chosen, fitness_chosen)][0] += 1
            else:
                bad_memes_select_nums[(quality_chosen, fitness_chosen)][1] += 1

        # diffuse meme's quality
        temp_quality = quality_nodescreen[affectednodes, :screen_size-1].copy()
        lastmemes_quality = quality_nodescreen[affectednodes, screen_size-1]
        quality_nodescreen[affectednodes, 0] = quality_chosen
        quality_nodescreen[affectednodes, 1:] = temp_quality

        # diffuse meme's fitness
        temp_fitness = fitness_nodescreen[affectednodes, :screen_size-1].copy()
        lastmemes_fitness = fitness_nodescreen[affectednodes, screen_size-1]
        fitness_nodescreen[affectednodes, 0] = fitness_chosen
        fitness_nodescreen[affectednodes, 1:] = temp_fitness

        # last memes
        lastmemes = set()
        for lq, lf in zip(lastmemes_quality, lastmemes_fitness):
            if lq == 0:
                lastmeme = (lq, lf)
            else:
                lastmeme = (lq, 0) # if lq=0, then lf is not important, set lf=0
            lastmemes.add(lastmeme)


        # record something
        #each_step_nodes_contain_bad_memes.append(np.sum(np.sum(quality_nodescreen[:n, :]==0, axis=1)>=1))
        #each_step_bad_memes_nums.append(np.sum(quality_nodescreen[:n, :]==0))
        #each_step_select_node.append(select_one_node)
        #each_step_normal_nodes_avg_quality_steady2final[iter_].append(np.mean(quality_nodescreen[:n, :]))

        # remove memes not found anywhere in the n/w
        for lq, lf in lastmemes:
            if lq == 0:
                if np.all(lf != fitness_nodescreen[quality_nodescreen == lq]) and (lf != fitness_chosen and lq != quality_chosen) and ((lq, lf) in memes):
                    memes[(lq, lf)]['e'] = counter
                    if meme_dead < max_memes_track:
                        if memes[(lq, lf)]['s'] >= track_memes_after:
                            meme_dead += 1
                    if memes[(lq, lf)]['s'] < track_memes_after:
                        del memes[(lq, lf)]
                    if meme_dead + 1 == max_memes_track:
                        print "Maximum no. of requested memes dead at timestep: {}".format(counter)
            else:
                if np.all(lq != quality_nodescreen) and (lq != quality_chosen) and (lq in memes):
                    memes[lq]['e'] = counter
                    if meme_dead < max_memes_track:
                        if memes[lq]['s'] >= track_memes_after:
                            meme_dead += 1
                    if memes[lq]['s'] < track_memes_after:
                        del memes[lq]
                    if meme_dead + 1 == max_memes_track:
                        print "Maximum no. of requested memes dead at timestep: {}".format(counter)

        if len(memes) > max_meme_size:
            max_meme_size = len(memes)

        # update meme set
        if quality_chosen == 0:
            if (quality_chosen, fitness_chosen) in memes:
                memes[(quality_chosen, fitness_chosen)]['n'] = memes[(quality_chosen, fitness_chosen)]['n'] + 1
            else:
                if counter >= track_memes_after:
                    meme_count += 1
                memes[(quality_chosen, fitness_chosen)] = {'s': counter, 'e': 1, 'n': 1}
        else:
            if quality_chosen in memes:
                memes[quality_chosen]['n'] = memes[quality_chosen]['n'] + 1
            else:
                if counter >= track_memes_after:
                    meme_count += 1
                memes[quality_chosen] = {'s': counter, 'e': 1, 'n': 1}
        if meme_dead == max_memes_track:
            break

        # TRICK: delete memes that live too long with selected_num=1
        #if len(memes) > track_memes_after*2 and counter % 10**3 == 0:
        #    for meme_ in memes.keys():
        #        if counter - memes[meme_]['s'] > 10**3 and memes[meme_]['e'] == 1 and memes[meme_]['n'] == 1:
        #            del memes[meme_]

    print "{}-th simulations completes.., Elapsed time: {}".format(iter_+1, time.time()-t1)

    ### save current simulation datas ###
    for meme_ in memes.keys():
        if memes[meme_]['s'] < track_memes_after or memes[meme_]['e'] == 1:
            del memes[meme_]
    memes_all.append(memes)

    bad_memes_select_nums_all.append(bad_memes_select_nums)
    bad_meme_propagation_path_all.append(bad_meme_propagation_path)

    if not os.path.exists(results_save_to + '/{}'.format(iter_)):
        os.mkdir(results_save_to + '/{}'.format(iter_))

    fp = open(results_save_to + '/{}/final_quality_nodescreen_{}_{}_{}_{}_{}_{}_{}_{}.pkl'.format(iter_, n, m, p, percent_bots, wire, phi, alpha, mu), 'wb')
    pickle.dump(quality_nodescreen, fp)
    fp.close()

    fp = open(results_save_to + '/{}/final_fitness_nodescreen_{}_{}_{}_{}_{}_{}_{}_{}.pkl'.format(iter_, n, m, p, percent_bots, wire, phi, alpha, mu), 'wb')
    pickle.dump(fitness_nodescreen, fp)
    fp.close()
    ### end current simulation datas ###

#fp = open(results_save_to + '/each_step_normal_nodes_avg_quality_steady2final_{}_{}_{}_{}_{}_{}_{}_{}.pkl'.format(n, m, p, percent_bots, wire, phi, alpha, mu), 'wb')
#pickle.dump(each_step_normal_nodes_avg_quality_steady2final, fp)
#fp.close()

endtime = time.time()
print "Done! Total time in seconds: {}".format((endtime - starttime))


# ==============================================================
# meme statistics
# ==============================================================
print "\n{} out of {} requested memes were born and dead after {} steady step".format(map(len, memes_all), max_memes_track, track_memes_after)
print "Size of all memes (in MBs): {}".format(sys.getsizeof(memes_all) / float(1024**2))
print "Max meme size: {}".format(max_meme_size)
print "saving meme statistics..."


### meme quality&popularity process ###
quality_all = []
number_selected_all = []
for memes in memes_all:
    for meme, val in memes.iteritems():
        if isinstance(meme, tuple):
            quality_all.append(meme[0]) # if zero quality meme, then only get the quality
        else:
            quality_all.append(meme)
        number_selected_all.append(val['n'])

qualityVspopularity = zip(quality_all, number_selected_all)
fp = open(results_save_to + '/tracked_memes_quality_and_popularity_{}_{}_{}_{}_{}_{}_{}_{}.pkl'.format(n, m, p, percent_bots, wire, phi, alpha, mu), 'wb')
pickle.dump(qualityVspopularity, fp)


### bad meme selected process ###
fit = []
good_sel = []
bad_sel = []
for sel in bad_memes_select_nums_all:
    for key, val in sel.iteritems():
        fit.append(key[1]) # fitness of bad meme(quality=0)
        good_sel.append(val[0])
        bad_sel.append(val[1])

bad_meme_sel_data = zip(fit, good_sel, bad_sel)
fp = open(results_save_to + '/bad_meme_selected_data_{}_{}_{}_{}_{}_{}_{}_{}.pkl'.format(n, m, p, percent_bots, wire, phi, alpha, mu), 'wb')
pickle.dump(bad_meme_sel_data, fp)


### normal node bad meme selected process ###
normal_node_bad_memes_select_nums_final = dict()
for key, val in normal_node_bad_memes_select_nums.iteritems():
    normal_node_bad_memes_select_nums_final[key] = [val[0], val[1]*1.0/times] # times=5

fp = open(results_save_to + '/normal_node_bad_meme_sel_{}_{}_{}_{}_{}_{}_{}_{}.pkl'.format(n, m, p, percent_bots, wire, phi, alpha, mu), 'wb')
pickle.dump(normal_node_bad_memes_select_nums_final, fp)
fp.close()


### bad meme propagation path (only normal node) ###
fp = open(results_save_to + '/bad_meme_propagation_path_{}_{}_{}_{}_{}_{}_{}_{}.pkl'.format(n, m, p, percent_bots, wire, phi, alpha, mu), 'wb')
pickle.dump(bad_meme_propagation_path_all, fp)
fp.close()


### each step infos process ###
fp = open(results_save_to + '/each_step_nodes_contain_bad_memes_{}_{}_{}_{}_{}_{}_{}_{}.pkl'.format(n, m, p, percent_bots, wire, phi, alpha, mu), 'wb')
pickle.dump(each_step_nodes_contain_bad_memes, fp)
fp.close()

fp = open(results_save_to + '/each_step_bad_memes_nums_{}_{}_{}_{}_{}_{}_{}_{}.pkl'.format(n, m, p, percent_bots, wire, phi, alpha, mu), 'wb')
pickle.dump(each_step_bad_memes_nums, fp)
fp.close()

fp = open(results_save_to + '/each_step_select_node_{}_{}_{}_{}_{}_{}_{}_{}.pkl'.format(n, m, p, percent_bots, wire, phi, alpha, mu), 'wb')
pickle.dump(each_step_select_node, fp)
fp.close()


### kendall process ###
q_p_dict = defaultdict(list)
for memes in memes_all:
    for meme, val in memes.iteritems():
        q_p_dict[meme].append(val['n'])

quality = []
population = []
for meme, selected_nums in q_p_dict.iteritems():
    if isinstance(meme, tuple):
        quality.append(meme[0]) # quality=0
    else:
        quality.append(meme)
    population.append(np.mean(selected_nums))

kendall, p1 = stats.kendalltau(quality, population)
fp = open(os.path.join(results_save_to, 'kendall_{}_{}_{}_{}_{}_{}_{}_{}.txt'.format(n, m, p, percent_bots, wire, phi, alpha, mu)), 'w')
print >> fp, "kendalltau:{}, p:{}".format(kendall, p1)
fp.close()

low_quality_pop = []
high_quality_pop = []
for qua, pop in zip(quality, population):
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

plt.figure(2)
plt.loglog(h_mids, h_heights, marker='s', label='high quality')
plt.loglog(l_mids, l_heights, marker='^', label='low quality')
plt.xlabel("popularity")
plt.ylabel("P(popularity)")
plt.legend(loc="upper right")
plt.savefig(results_save_to + '/meme_quality_distr_{}_{}_{}_{}_{}_{}_{}_{}.png'.format(n, m, p, percent_bots, wire, phi, alpha, mu))
plt.close()
print "saved meme statistics."
