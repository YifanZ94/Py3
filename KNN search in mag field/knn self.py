# -*- coding: utf-8 -*-
"""
Created on Tue Jan  5 18:15:40 2021

@author: Administrator
"""
import os
import numpy as np
import math 
import time 

os.chdir('F:\py code\Py3\KNN search in mag field')

B = np.load('BMap.npy')
LocMap = np.load('LocMap.npy')
testSample = np.load('testSample.npy')
NormP = np.load('NormParameter.npy')

#%%

def nearestN(field, measure): 
    dis_list = []
    for i in range(len(field)):
        point = field[i]
        dis_list.append((measure[0]-point[0])**2+(measure[1]-point[1])**2+(measure[2]-point[2])**2)
        
    return dis_list.index(min(dis_list))
                
#%%
begin = time.time()
loc_list = []
L = len(testSample)
location = np.zeros((L,3))
j = 0
for i in testSample:
    Normliezed = [(i[0]-NormP[0][0])/NormP[0][3],(i[1]-NormP[0][1])/NormP[0][4],(i[2]-NormP[0][2])/NormP[0][5]]
    I = nearestN(B,Normliezed )
    location[j,:] = LocMap[I]
    j += 1

end = time.time()
runTime = end - begin
#%%
import matplotlib.pyplot as plt

xRef = np.linspace(-15,15,num=L)
yRef = np.linspace(5.2, 8.2, num=L)
zRef = -18*np.ones((L,1))

plt.plot(xRef,location[:,0])
plt.show()
plt.plot(yRef,location[:,1])
plt.show()
plt.plot(xRef,location[:,2])
plt.show()