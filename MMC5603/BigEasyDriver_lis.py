# -*- coding: utf-8 -*-
"""
Created on Sun Aug  2 16:30:07 2020

@author: user
"""
import os 
os.environ["BLINKA_FT232H"] = "1"
os.chdir('F:/py code/Python3/MMC5603')

import board
import digitalio
import mag_data_py3_lis
import time
import fileinput

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

filename = input('enter the file name: ')
data1File = open(filename + 'MMC.txt', 'w')
#envFile = open(filename + 'env.txt', 'w')

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
    
#%% initialization
#
MMC = mag_data_py3_lis.I2C_mag()
MMC.all_data()

data = [MMC.all_data()]
distance = [0]

#%%  start measuring

direc.value = True

for i in range(10):
    move(steps)
    time.sleep(0.2)
    data.append(MMC.all_data())
    distance.append(distance[-1] + disIncrement)
    
#%%     return
direc.value = False
move(round(steps*disRange/disIncrement))
# MMC.finish
#%%
