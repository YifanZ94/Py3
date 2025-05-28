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
data = []
sensor.acceleration
sensor.gyro
time.sleep(1)

sleepT = 0.01
print('start')
while True:
    try:
        accel_x, accel_y, accel_z = sensor.acceleration
        gyro_x, gyro_y, gyro_z = sensor.gyro
        # mag_x, mag_y, mag_z = sensor.magnetic
        data.append([accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z])
    except:
        break

duration = time.time()-start
print(duration)
filename = input('enter the file name: ')       
file = open(filename + '_IMU.txt', 'w')
np.savetxt(file, np.array(data))
file.close()

#%%
import matplotlib.pyplot as plt
x = np.arange(len(data))
y = np.array(data)
plt.plot(x,y[:,2])
plt.show()
plt.close()