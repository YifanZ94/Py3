# -*- coding: utf-8 -*-
"""
Created on Sun Aug  2 16:30:07 2020

@author: user
"""
import os 
os.environ["BLINKA_FT232H"] = "1"
# os.chdir('F:/py code/Python3/MMC5603')

import board
import digitalio
import time
import mag_data_py3

#%%   GPIO setup
enable = digitalio.DigitalInOut(board.D5)
enable.direction = digitalio.Direction.OUTPUT

direc = digitalio.DigitalInOut(board.D6)
direc.direction = digitalio.Direction.OUTPUT

step = digitalio.DigitalInOut(board.D7)
step.direction = digitalio.Direction.OUTPUT

MS1 = digitalio.DigitalInOut(board.C0)
MS1.direction = digitalio.Direction.OUTPUT

MS2 = digitalio.DigitalInOut(board.C1)
MS2.direction = digitalio.Direction.OUTPUT

MS3 = digitalio.DigitalInOut(board.C2)
MS3.direction = digitalio.Direction.OUTPUT


#%%

stepdelay = 0.001
MS1.value = False
MS2.value = True
MS3.value = False

disRange = 10
disIncrement = 1
steps = round(disIncrement*3*250/5.08)

def move(steps):
    enable.value = False
    
    for i in range(steps):
        step.value = True
        time.sleep(stepdelay)

        step.value = False
        time.sleep(stepdelay)
        
    enable.value = True

print('motor ready')
#%% initialization


MMC = mag_data_py3.I2C_mag()
print('sensor ready')

data = [MMC.all_data()]

print(data)

distance = [0]
    
#%%  start measuring

direc.value = True

for i in range(10):
    move(steps)
    time.sleep(0.2)
    distance.append(distance[-1] + disIncrement)
    
#%%     return
direc.value = False
move(round(steps*disRange/disIncrement))

#%%
