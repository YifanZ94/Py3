# -*- coding: utf-8 -*-
"""
Created on Mon Feb 15 14:07:53 2021

@author: Administrator
"""
import os 
# os.environ["BLINKA_MCP2221"] = "1"
os.environ["BLINKA_FT232H"] = "1"         # different microcontroller

import board
import time
import digitalio

enable = digitalio.DigitalInOut(board.C0)
enable.direction = digitalio.Direction.OUTPUT
direc = digitalio.DigitalInOut(board.C2)
direc.direction = digitalio.Direction.OUTPUT
step = digitalio.DigitalInOut(board.C1)
step.direction = digitalio.Direction.OUTPUT
MS1 = digitalio.DigitalInOut(board.D6)
MS1.direction = digitalio.Direction.OUTPUT
MS2 = digitalio.DigitalInOut(board.D7)
MS2.direction = digitalio.Direction.OUTPUT

MS1.value = False
MS2.value = True

disRange = 10
disIncrement = 1
# steps = round(disIncrement*135)

class motor:
    def __init__(self):
        self.stepdelay = 5e-3
        # MS1.value = False
        # MS2.value = True
        
    def move_one_step(self,dirIn): 
        if dirIn == 0:
            direc.value = True
        else:
            direc.value = False
        enable.value = False
        step.value = True
        time.sleep(self.stepdelay)
        step.value = False
        time.sleep(self.stepdelay)
        
        
    def move(self,dist,dirIn): 
        if dirIn == 0:
            direc.value = True
        else:
            direc.value = False
        enable.value = False

        self.steps = round(dist*3*250/5.3)
        for i in range(self.steps):
            step.value = True
            time.sleep(self.stepdelay)
            step.value = False
            time.sleep(self.stepdelay)
            
        enable.value = True

Motor = motor()
for i in range(4):
    Motor.move(2,0)
    time.sleep(0.5)