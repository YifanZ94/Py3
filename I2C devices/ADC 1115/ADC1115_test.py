# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 15:34:24 2023

@author: Administrator
"""

import os 
os.environ["BLINKA_FT232H"] = "1" 

import board
import busio
import time
import numpy as np
i2c = busio.I2C(board.SCL, board.SDA)

import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

ads = ADS.ADS1115(i2c)
chan = AnalogIn(ads, ADS.P0, ADS.P3)

V_list = []
print('start')

while True:
    try:
        V = chan.voltage
        V_list.append(V)
        print("the voltage is "+ str(round(V,2)) + "V")
        time.sleep(0.2)
    except:
        break
    
# filename = input('enter the file name: ')
# file = open(filename +'_force.txt', 'w')
# np.savetxt(file, np.array(V_list))
# file.close()
    