# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 22:02:40 2020

@author: Administrator
"""

import os 
os.environ["BLINKA_FT232H"] = "1"

import time
import mag_data_py3_lis

sensor = mag_data_py3_lis.I2C_mag()

while True:
    data = sensor.all_data()
 
    print(data)
    print("")
    time.sleep(1.0)