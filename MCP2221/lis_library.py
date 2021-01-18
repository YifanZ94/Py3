# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 22:02:40 2020

@author: Administrator
"""

import os 
os.environ["BLINKA_MCP2221"] = "1"

import time
import board
import busio
import adafruit_lis2mdl
 
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_lis2mdl.LIS2MDL(i2c)
 
while True:
    mag_x, mag_y, mag_z = sensor.magnetic
 
    print("X:{0:10.2f}, Y:{1:10.2f}, Z:{2:10.2f} uT".format(mag_x, mag_y, mag_z))
    print("")
    time.sleep(1.0)