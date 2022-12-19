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
import adafruit_lsm9ds0
import numpy as np

# I2C connection:
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_lsm9ds0.LSM9DS0_I2C(i2c)

start = time.time()
i = 0
gyro_list = []

def measure():
    acc = sensor.acceleration
    return [acc[0] + 0.72, acc[1] - 0.24, acc[2] + 0.2]

sleepT = 0.05
print('start')
for i in range(20):
    gyro_list.append(measure())
    time.sleep(sleepT)

filename = input('enter the file name: ')       
file = open(filename + '_3in1.txt', 'w')
np.savetxt(file, np.array(gyro_list))
file.close()
