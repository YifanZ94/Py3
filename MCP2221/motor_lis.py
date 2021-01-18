"""
Created on Mon Jun 29 22:02:40 2020

@author: Administrator
"""

import os 
os.environ["BLINKA_MCP2221"] = "1"

import board
import digitalio
import time
import busio
import adafruit_lis2mdl


#%%   GPIO setup
enable = digitalio.DigitalInOut(board.G2)
enable.direction = digitalio.Direction.OUTPUT

direc = digitalio.DigitalInOut(board.G1)
direc.direction = digitalio.Direction.OUTPUT

step = digitalio.DigitalInOut(board.G0)
step.direction = digitalio.Direction.OUTPUT

#%%

stepdelay = 0.001

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

i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_lis2mdl.LIS2MDL(i2c)

#%%  start measuring

direc.value = True

for i in range(10):
    move(steps)
    mag_x, mag_y, mag_z = sensor.magnetic
 
    print("X:{0:10.2f}, Y:{1:10.2f}, Z:{2:10.2f} uT".format(mag_x, mag_y, mag_z))
    print("")
    
    time.sleep(0.5)
    
#%%     return
direc.value = False
move(round(steps*disRange/disIncrement))