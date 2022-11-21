# -*- coding: utf-8 -*-
"""
Created on Wed Feb  3 16:22:27 2021

@author: Administrator
"""

import board
import time
import digitalio

enable = digitalio.DigitalInOut(board.D17)
enable.direction = digitalio.Direction.OUTPUT
direc = digitalio.DigitalInOut(board.D23)
direc.direction = digitalio.Direction.OUTPUT
step = digitalio.DigitalInOut(board.D24)
step.direction = digitalio.Direction.OUTPUT
MS1 = digitalio.DigitalInOut(board.D5)
MS1.direction = digitalio.Direction.OUTPUT
MS2 = digitalio.DigitalInOut(board.D6)
MS2.direction = digitalio.Direction.OUTPUT

stepdelay = 0.001
MS1.value = False
MS2.value = True
enable.value = True

class motor:
    def __init__(self):
#         self.enable = enable
#         self.direc = direc
#         self.step = step
#         self.MS1 = MS1
#         self.MS2 = MS2
        
        self.stepdelay = 0.001
#         MS1.value = False
#         MS2.value = True
        
    def move(self,steps,direc_in):
        if direc_in == 0:
            direc.value = True
        else:
            direc.value = False
        enable.value = False
        
        for i in range(steps):
            step.value = True
            time.sleep(self.stepdelay)
            step.value = False
            time.sleep(self.stepdelay)
            
        enable.value = True


# Motor = motor()
# dis_increment = 5
# Motor.move(round(dis_increment*3*250/5.3),1)
# print('done')