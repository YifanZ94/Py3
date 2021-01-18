# -*- coding: utf-8 -*-
"""
Created on Tue Jan  5 12:24:52 2021

@author: Administrator
"""
import os
os.chdir('F:\py code\Py3\KNN search in mag field')

import scipy.io as sio
field = sio.loadmat('Map.mat')
test = sio.loadmat('test.mat')

import numpy as np
import math
from sklearn.neighbors import NearestNeighbors
import time 
#%%
locMap = np.concatenate((field["xR"],field["yR"],field["zR"]), axis=1)
B = np.concatenate((field["BxR2"],field["ByR2"],field["BzR2"]), axis=1)
NormParameter = np.concatenate((field["xMin"],field["yMin"],field["zMin"],field["demX"],field["demY"],field["demZ"]), axis=1)

begin = time.time()
neigh = NearestNeighbors(n_neighbors=1)
neigh.fit(B)

#%%

testSample = test["magH"]
L = len(testSample)
location = np.zeros((L,3))
theta = math.atan(15/140)
j = 0
for i in testSample:
    measure_R = [i[0]*math.cos(theta)-i[1]*math.sin(theta), i[0]*math.sin(theta)+i[1]*math.cos(theta), i[2]]
    index = neigh.kneighbors([measure_R], 1, return_distance=False)
    location[j,:] = locMap[index]
    j += 1
    
end = time.time()
runTime = end - begin
#%%
import matplotlib.pyplot as plt
xRef = np.linspace(-15,15,num=L)
yRef = np.linspace(5.2, 8.2, num=L)
zRef = -18*np.ones((L,1))
plt.subplot(3,1,1)
plt.plot(xRef,location[:,0])
plt.subplot(3,1,2)
plt.plot(yRef,location[:,1])
plt.subplot(3,1,3)
plt.plot(xRef,location[:,2])
plt.show()

#%%