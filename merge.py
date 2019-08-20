#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: rosdays

@description: merge each time's data
"""

import sys
import glob
import cPickle as pickle
from collections import defaultdict


if sys.argv[1] == '-h':
    print 'Usage:command "data path wildcard"'
    print 'Example:python merge.py "0.5_result_datas/bad_meme_select_datas_*"'
    sys.exit(0)

fmatch = sys.argv[1]
print fmatch
fnames = sorted(glob.glob(fmatch))
print 'merging {}'.format(fnames)
prefix = -1
for idx, c in enumerate(fnames[-1][::-1]):
    if c == '_':
        prefix = idx+1
        break
fmerge = fnames[-1][:-prefix]+'.pkl'

data = defaultdict(list)
for fname in fnames:
    fp = open(fname, 'rb')
    d = pickle.load(fp)
    fp.close()
    for k, v in d.iteritems():
        data[k].append(v)
fw = open(fmerge, 'wb')
pickle.dump(data, fw)
fw.close()
