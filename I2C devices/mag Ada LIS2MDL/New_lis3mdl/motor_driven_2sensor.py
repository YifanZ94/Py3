# -*- coding: utf-8 -*-
"""
Created on Sun Jan 17 18:51:18 2021

@author: Administrator
"""
import numpy as np
import matplotlib.pyplot as plt
import time
import board
import digitalio
i2c = board.I2C()

from MotorDriver import motor
import adafruit_lis3mdl
import adafruit_lis3mdl_H

Motor = motor()
MAG2= adafruit_lis3mdl.LIS3MDL(i2c)
MAG = adafruit_lis3mdl_H.LIS3MDL(i2c)

## setting
dis_total = 20
dis_increment = 1
sleepT = 0.5
steps = round(dis_increment*125)
data_points = int(dis_total/dis_increment)

#%%  start measuring
relay = digitalio.DigitalInOut(board.D12)
relay.direction = digitalio.Direction.OUTPUT
data1 = []
data2 = []
location = []
print('ready')

for i in range(data_points+1):
    relay.value = 0
    time.sleep(sleepT)
    env1 = np.array(MAG.magnetic)
    env2 = np.array(MAG2.magnetic)
    relay.value = 1
    time.sleep(sleepT)
    reading1 = np.array(MAG.magnetic) - env1
    reading2 = np.array(MAG2.magnetic) - env2
    relay.value = 0
    data1.append(reading1)
    data2.append(reading2)
    time.sleep(sleepT)
    Motor.move(steps,1)

#%%     return
relay.value = 0
direc = 0
Motor.move(steps*data_points,0)

#%% plot
# x = np.arange(len(data1))
# npData = np.array(data1)
# plt.plot(x,npData[:,0])
# plt.show()

#%%  save the data
filename = input('enter the file name ')
file = open(filename + '_Magn1.txt', 'w')
np.savetxt(file, np.array(data1))
file.close()

file = open(filename + '_Magn2.txt', 'w')
np.savetxt(file, np.array(data2))
file.close()