# -*- coding: utf-8 -*-
"""
Created on Fri Mar 19 17:24:56 2021

@author: Administrator
"""

# import os
# os.chdir('F:\py code\Py3\working directory')

import numpy as np
from sklearn.neighbors import NearestNeighbors

B = np.load('BMap.npy')
LocMap = np.load('LocMap.npy')
NormP = np.load('NormP.npy')

#%%

class KNN:
    def __init__(self):
        self.neigh = NearestNeighbors(n_neighbors=1, algorithm='brute')
        self.neigh.fit(B)
        
    def search(self,measure):
        self.theta = 0
        self.Normliezed = [(measure[0]-NormP[0][3])/NormP[0][0],
                           (measure[1]-NormP[0][4])/NormP[0][1],
                           (measure[2]-NormP[0][5])/NormP[0][2]]
        self.index = self.neigh.kneighbors([self.Normliezed], 1, return_distance=False)
        return  LocMap[self.index]
    
    
class KNN_self:
    # def __init__(self):
        
    def search(self,measure):
        self.Normliezed = [(measure[0]-NormP[0][3])/NormP[0][0],
                            (measure[1]-NormP[0][4])/NormP[0][1],
                            (measure[2]-NormP[0][5])/NormP[0][2]]
        
        # self.dist_min = 1000
        # self.index = 0
        # self.index_min = 0
        self.D = np.zeros(len(B))
        for i in range(10):
            self.D[i] = (self.Normliezed[0]- B[i][0])**2+(self.Normliezed[1]- B[i][1])**2+(self.Normliezed[2]- B[i][2])**2      
        
        self.index = np.argmin(self.D)
        return  LocMap[self.index]
#%%
import matplotlib.pyplot as plt
import time
test = np.load('t1_mag.npy')
ref = np.load('t1_loc.npy')
location = []

start = time.time()
alg = KNN_self()

for i in test:
    loc = alg.search(i)
    # location.append([loc[0][0][0],loc[0][0][1],loc[0][0][2]])
    location.append(loc)
    
end = time.time()
x = np.arange(len(test))
npData = np.array(location)
plt.plot(npData[:,0], label="redo")
plt.plot(ref[:,0], label="measure")
plt.legend()
plt.show() 
print(end-start)   