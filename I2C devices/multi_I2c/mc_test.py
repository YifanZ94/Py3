# -*- coding: utf-8 -*-
"""
Created on Sun May  2 18:28:59 2021

@author: Administrator
"""

import os 
os.environ["BLINKA_FT232H"] = "1"         # different microcontroller

import time
import board
import numpy as np
# i2c = board.I2C()

i2c =  board.I2C()


#%%  IMU

# import adafruit_lsm9ds0
# sensor = adafruit_lsm9ds0.LSM9DS0_I2C(tca[7])
# start = time.time()
# i = 0
# gyro_list = []

# def measure():
#     gyro_x, gyro_y, gyro_z = sensor.acceleration
#     return [gyro_x + 0.72, gyro_y - 0.24, gyro_z + 0.2]

# sleepT = 0.2
# print('start')
# for i in range(200):
#     print(measure())
#     time.sleep(sleepT)

#%%  acc stephanie

# import mxc4005xc
# sensor = mxc4005xc.MXC4005XC(tca[1])
# start = time.time()
# i = 0
# gyro_list = []

# while True:
#     time.sleep(0.5)
#     # accdata1 = acc1.acceleration
#     accdata = sensor.acceleration
#     # print("MC3672: {0}".format(accdata1))
#     print("MXC4005XC: {0}".format(accdata))

#%%
import adafruit_tca9548a
tca = adafruit_tca9548a.TCA9548A(i2c)

import MMC5603
mag1 = MMC5603.Mag(tca[2])
# mag2 = MMC5603.Mag(tca[2])

# print('ready to go')

# while True:
#     # try:
#         # ans1.append(mag1.all_data())
#     print(mag1.all_data())
#     time.sleep(0.5)
    # except:
    #     break