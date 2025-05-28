# -*- coding: utf-8 -*-
"""
Created on Tue Mar 23 19:14:39 2021

@author: Administrator
"""

import os 
os.environ["BLINKA_FT232H"] = "1" 
# os.chdir('F:\py code\Py3\I2C devices\IMU_LSM9DS0')

import time
import board
import busio 
import numpy as np
# import mc3672
import mxc4005xc
# I2C connection:
i2c = busio.I2C(board.SCL, board.SDA)
sensor = mxc4005xc.MXC4005XC(i2c)

start = time.time()
i = 0
s1_list = []

sleepT = 0.02
print('start')
sample_size = 10

ind = 0
direc = ["0 -g 0","0 0 -g","g 0 0","0 g 0","-g 0 0","0 0 g"]
while True:
    if ind>= 6:
        print('done')
        break
    
    print(direc[ind])
    com = input("now is the {} th position, enter n to quit ".format(ind+1))
    ind += 1
    if com == 'n':
        break
    else:
        for i in range(sample_size):
            reading = sensor.acceleration
            s1_list.append(reading)
            # s2_list.append(sensor2.raw_data())
            # s3_list.append(sensor3.acceleration())
            time.sleep(sleepT)

#%%
s1_array = np.array(s1_list)     
ave = []   
for i in range(6):
    ave.append(np.mean(s1_array[i*10:(i+1)*10,], axis=0))

#%%
ave = np.array(ave)/9.81
B = np.array([[ave[0][0]+ave[1][0]+ave[3][0]+ave[5][0]],
              [ave[1][1]+ave[2][1]+ave[4][1]+ave[5][1]],
              [ave[0][2]+ave[2][2]+ave[3][2]+ave[5][2]]])/4

S = np.array([[ave[2][0]-ave[4][0], ave[3][0]-ave[0][0], ave[5][0]-ave[1][0]],
             [ave[2][1]-ave[4][1], ave[3][1]-ave[0][1], ave[5][1]-ave[1][1]],
             [ave[2][2]-ave[4][2], ave[3][2]-ave[0][2], ave[5][2]-ave[1][2]]])/2

S_inv = np.linalg.inv(S)
#%%
def calibrate(measure):
    h = np.reshape(measure,(3,1))
    return np.matmul(S_inv,(h-B))

s1_calied = []
for i in s1_array:
    s1_calied.append(calibrate(i))
    
#%%
mag_1 = []
mag_2 = []
x_off = 0
y_off = 0
z_off = 2
for i in range(60):
    s1_calied[i] = s1_array[i] + [x_off,y_off,z_off]
    mag_1.append(np.linalg.norm(s1_calied[i]))
    
#%%
    
# filename = input('enter the file name: ')       
# file = open(filename + '_accS.txt', 'w')
# np.savetxt(file, np.array(s1_list))
# file.close()

# file = open(filename + '_acc.txt', 'w')
# np.savetxt(file, np.array(s2_list))
# file.close()

# file = open(filename + '_acc_S.txt', 'w')
# np.savetxt(file, np.array(s3_list))
# file.close()
