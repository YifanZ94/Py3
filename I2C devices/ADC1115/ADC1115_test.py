# -*- coding: utf-8 -*-
"""
Created on Mon Oct 24 19:03:03 2022

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
chan = AnalogIn(ads, ADS.P3)

def forceReading(voltage):
    if voltage == 0:
        fsrForce = 0
    else:
        V = voltage*1000
        R_fsr = (5000 - V)*10000/V
        fsrConductance = 1000000/R_fsr
        
        if fsrConductance <= 1000:
            fsrForce = fsrConductance / 80
        else:
            fsrForce = (fsrConductance - 1000)/30
            
    return fsrForce

V_list = []
F_list = []
print('start')

while True:
    try:
        V = chan.voltage
        V_list.append(V)
        force = forceReading(V)
        F_list.append(force)
        # print("the voltage is "+ str(round(V,2)) + "V")
        # print("the force is " + str(round(force,2)) + "N")
        time.sleep(0.02)
    except:
        break
    
filename = input('enter the file name: ')
file = open(filename +'_force.txt', 'w')
np.savetxt(file, np.array(F_list))
file.close()
    
# V = chan.voltage
# force = forceReading(V)
# # /0.0098
# print("the force is " + str(force*101.9) + "gram")