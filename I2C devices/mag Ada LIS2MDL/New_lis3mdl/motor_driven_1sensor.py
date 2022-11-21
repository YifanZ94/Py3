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

Motor = motor()
MAG = adafruit_lis3mdl.LIS3MDL(i2c)

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
location = []
print('ready')

for i in range(data_points+1):
    relay.value = 0
    time.sleep(sleepT)
    env1 = np.array(MAG.magnetic)
    relay.value = 1
    time.sleep(sleepT)
    reading1 = np.array(MAG.magnetic) - env1
    relay.value = 0
    data1.append(reading1)
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
file = open(filename + '__lis3mdl.txt', 'w')
np.savetxt(file, np.array(data1))
file.close()
