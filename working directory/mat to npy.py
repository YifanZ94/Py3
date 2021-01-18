# -*- coding: utf-8 -*-
"""
Created on Mon Jan 18 16:21:23 2021

@author: Administrator
"""

import os
os.chdir('F:\py code\Py3\working directory')
import numpy as np
import scipy.io as sio

test = sio.loadmat('env.mat')
env = test['data']
