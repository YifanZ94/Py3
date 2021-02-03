# -*- coding: utf-8 -*-
"""
Created on Mon Jan 18 16:21:23 2021

@author: Administrator
"""

import os
os.chdir('F:\py code\Py3\working directory')
import numpy as np
import scipy.io as sio

test = sio.loadmat('elecMap.mat')
norm = sio.loadmat('normPara.mat')
B = np.hstack((np.transpose(test['BxR2']),np.transpose(test['ByR2']),np.transpose(test['BzR2'])))
LocMap = np.hstack((test['xR'],test['yR'],test['zR']))
NormP = norm['p']

np.save('B',B)
np.save('LocMap',LocMap)
np.save('NormP',NormP)

# B = np.load('B.npy')