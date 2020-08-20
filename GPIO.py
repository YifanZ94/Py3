# -*- coding: utf-8 -*-

"""
Created on Tue Jun 30 13:32:48 2020

@author: Administrator
"""

import os 
os.environ["BLINKA_FT232H"] = "1"

import time
import board
import digitalio
 
led = digitalio.DigitalInOut(board.C0)
led.direction = digitalio.Direction.OUTPUT
 
while True:
    led.value = True
    time.sleep(0.5)
    led.value = False
    time.sleep(0.5)
