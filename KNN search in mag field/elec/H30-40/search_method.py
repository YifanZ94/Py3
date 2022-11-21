# -*- coding: utf-8 -*-
"""
Created on Fri Mar 19 17:24:56 2021

@author: Administrator
"""

import os
os.chdir('F:\py_code\Py3\KNN search in mag field\elec\H30-40')

import numpy as np
from sklearn.neighbors import NearestNeighbors

# B = np.load('B.npy')     ## map height 10-30
# LocMap = np.load('LocMap.npy')
# NormP = np.load('NormP.npy')

C = (181/115)*1.5/2.1
C = 1
B = C*np.load('H30-40_B.npy')             # (working I/ref)
LocMap = np.load('H30-40_LocMap.npy')
NormP = C*np.load('H30-40_NormP.npy')

#%%

class KNN:
    def __init__(self):
        self.neigh = NearestNeighbors(n_neighbors=1, algorithm='brute', n_jobs=-1)
        self.neigh.fit(B)
        
    def search(self,measure):
        self.theta = 0
        self.Normliezed = [(measure[0]-NormP[0][3])/NormP[0][0],
                           (measure[1]-NormP[0][4])/NormP[0][1],
                           (measure[2]-NormP[0][5])/NormP[0][2]]
        self.D, self.index = self.neigh.kneighbors([self.Normliezed], 1, return_distance=True)
        # return  LocMap[self.index]
        return self.D, self.index
    
    
class KNN_self:
    # def __init__(self):
        
    def search(self,measure):
        self.Normliezed = [(measure[0]-NormP[0][3])/NormP[0][0],
                            (measure[1]-NormP[0][4])/NormP[0][1],
                            (measure[2]-NormP[0][5])/NormP[0][2]]
        
        self.D = np.zeros(len(B))
        for i in range(len(B)):
            self.D[i] = (self.Normliezed[0]- B[i][0])**2+(self.Normliezed[1]- B[i][1])**2+(self.Normliezed[2]- B[i][2])**2      
        
        self.index = np.argmin(self.D)
        return self.D[self.index], self.index

    
# class KNN_dist:
#     # def __init__(self):
        
#     def search(self,measure):
#         self.Normliezed = [(measure[0]-NormP[0][3])/NormP[0][0],
#                             (measure[1]-NormP[0][4])/NormP[0][1],
#                             (measure[2]-NormP[0][5])/NormP[0][2]]
        
#         self.D = np.zeros(len(B))
#         for i in range(len(B)):
#             self.D[i] = np.linalg.norm(np.subtract(self.Normliezed, B[i]))      
        
#         self.index = np.argmin(self.D)
#         return  LocMap[self.index]

def normalize(measure):
    Normalized = [(measure[0]-NormP[0][3])/NormP[0][0],
                            (measure[1]-NormP[0][4])/NormP[0][1],
                            (measure[2]-NormP[0][5])/NormP[0][2]]
    return np.array(Normalized)


test = np.load('test.npy')
ref = np.load('ref_m.npy')
a = normalize(test[1])
D1 = np.linalg.norm(np.subtract(a, B[203748]))
D2 = np.linalg.norm(np.subtract(a, B[204207]))
    
#%%
import matplotlib.pyplot as plt
import time

ind1 = np.zeros((1,1))
ind2 = np.zeros((1,1))
d1 = np.zeros((1,1))
d2 = np.zeros((1,1))
L1 = np.zeros((1,3))
L2 = np.zeros((1,3))

start = time.time()
alg1 = KNN()
alg2 = KNN_self()

for i in test:

    a1,b1 = alg1.search(i)
    ind1 = np.vstack((ind1,b1))
    d1 = np.vstack((d1,a1))
    L1 = np.vstack((L1,LocMap[b1[0][0]]))
    
    a2,b2 = alg2.search(i)
    ind2 = np.vstack((ind2,b2))
    d2 = np.vstack((d2,a2))
    L2 = np.vstack((L2,LocMap[b1[0][0]]))

    # location.append([loc[0][0][0],loc[0][0][1],loc[0][0][2]])
    # location.append(loc)
    
end = time.time()

#%%
    
x = np.arange(len(test)+1)
L1Data = np.array(L1)
L2Data = np.array(L2)
plt.plot(x,L1Data[:,0], label="KNN")
plt.plot(x,L2Data[:,0], label="KNN_brute")
plt.plot(x[1:],ref[:,0], label="MAT")
plt.legend()
plt.show() 

print(end-start)   

#%%
filename = input('enter the file name ')
file = open(filename + '_ind.txt', 'w')
np.savetxt(file, np.array(ind1))
file.close()

file = open(filename + '_dis.txt', 'w')
np.savetxt(file, np.array(d1))
file.close()