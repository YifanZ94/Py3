# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 22:02:40 2020

@author: Administrator
"""

import os 
os.environ["BLINKA_FT232H"] = "1"

import time
import board
import busio
import MMC5603
 
i2c = busio.I2C(board.SCL, board.SDA)
sensor = MMC5603.MMC5603(i2c)
 
while True:
    sensor._enable = 1
    mag_x_L, mag_x_H = sensor.magnetic
    
    r = (mag_x_L << 8) + mag_x_H
    Gauss = (r/(65536.0) - 0.5)*60.0
    
    print("x1 =", mag_x_L, "x2 = ", mag_x_H)
    print("Gauss = ", Gauss)
    time.sleep(0.2)