# -*- coding: utf-8 -*-
"""
Created on Mon Oct 24 19:21:07 2022

@author: Administrator
"""

# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

""" Display magnetometer data once per second """
import os 
os.environ["BLINKA_FT232H"] = "1" 

import time
import board
import adafruit_lis3mdl

i2c = board.I2C()  # uses board.SCL and board.SDA
sensor = adafruit_lis3mdl.LIS3MDL(i2c)

while True:
    mag_x, mag_y, mag_z = sensor.magnetic

    print("X:{0:10.2f}, Y:{1:10.2f}, Z:{2:10.2f} uT".format(mag_x, mag_y, mag_z))
    print("")
    time.sleep(1.0)
