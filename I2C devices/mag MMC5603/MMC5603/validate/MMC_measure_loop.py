# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 19:34:13 2020

@author: Administrator
"""

import os 
os.environ["BLINKA_FT232H"] = "1"

import time
import board
import busio
import mag_data_py3

MMC = mag_data_py3.I2C_mag()

while True:
    time.sleep(1)
    print(MMC.all_data())

