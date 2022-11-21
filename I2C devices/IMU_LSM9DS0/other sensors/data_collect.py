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
import mc3672
import mxc4005xc
# I2C connection:
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_lsm9ds0.LSM9DS0_I2C(i2c)
sensor2 = mc3672.I2C_acc(i2c)
sensor3 = acc2 = mxc4005xc.MXC4005XC(i2c)

start = time.time()
i = 0
s1_list = []
s2_list = []
s3_list = []

def measure():
    gyro_x, gyro_y, gyro_z = sensor.acceleration
    return [gyro_x, gyro_y, gyro_z]

sleepT = 0.05
print('start')
for i in range(10):
    s1_list.append(measure())
    s2_list.append(sensor2.raw_data())
    s3_list.append(sensor3.acceleration())
    time.sleep(sleepT)


filename = input('enter the file name: ')       
file = open(filename + '_3in1.txt', 'w')
np.savetxt(file, np.array(s1_list))
file.close()

file = open(filename + '_acc.txt', 'w')
np.savetxt(file, np.array(s2_list))
file.close()