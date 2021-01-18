# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 22:02:40 2020

@author: Administrator
"""

import os 
# os.environ["BLINKA_MCP2221"] = "1"
os.environ["BLINKA_FT232H"] = "1"

import time
import board
import busio
import adafruit_lis2mdl
import mag_data_py3
 
i2c = busio.I2C(board.SCL, board.SDA)
LIS = adafruit_lis2mdl.LIS2MDL(i2c)
MMC = mag_data_py3.I2C_mag()
 
while True:
    mag_x, mag_y, mag_z = LIS.magnetic
 
    print("X:{0:10.2f}, Y:{1:10.2f}, Z:{2:10.2f} uT".format(mag_x, mag_y, mag_z))
    print("")
    
    data = MMC.get_data()
    print(data)
    print("")
    
    time.sleep(1.0)