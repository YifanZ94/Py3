# -*- coding: utf-8 -*-
"""
Created on Tue Mar 23 19:14:39 2021

@author: Administrator
"""

import os 
os.environ["BLINKA_FT232H"] = "1"         # different microcontroller

import time
import board
import numpy as np
i2c =  board.I2C()
import adafruit_tca9548a
tca = adafruit_tca9548a.TCA9548A(i2c)

#%%  IMU
import adafruit_lsm9ds1
sensor1 = adafruit_lsm9ds1.LSM9DS1_I2C(tca[0])
sensor2 = adafruit_lsm9ds1.LSM9DS1_I2C(tca[2])

start = time.time()

sensor1_data = []
sensor2_data = []

while True:
    try:
        sensor1_data.append(list(sensor1.acceleration))
        sensor2_data.append(list(sensor2.acceleration))
        time.sleep(0.01)
    except:
        break

end = time.time()
duration = end- start

print('end')