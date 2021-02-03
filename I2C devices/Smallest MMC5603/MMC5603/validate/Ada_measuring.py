# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 16:46:22 2019

@author: Stephanie

Modified from YEI 3-space example code
and Pololu High Power Stepper Driver example code
"""
#change the current working dirctory
#import os
#os.getcwd()
#os.chdir('C:\Users\Administrator\Desktop\py code\Python2\MMC5603')

import HighPowerStepperDriver
import time
import matplotlib.pyplot as plt
import fileinput
import numpy as np
import board
import digitalio
import mag_data_py3

#%%
#############################################################################
## CHANGE STEP SETTINGS AND FILE NAMES
#############################################################################

## MOTOR SETUP:
# current limit in milliamps
current = 2500
# stepper motor step size
stepMode = 'MicroStep4'
# stepper motor step delay
stepdelay = 0.001

## FILE NAMES:
# the program will save these in the same folder
# motor timestamp file
filename = input('enter the file name: ')
rawFile = open(filename + 'raw.txt', 'w')
envFile = open(filename + 'env.txt', 'w')
#disFile = open(filename + 'distance.txt','w')

time.sleep(1)

# initial distance is 0
motorDistance = 0
#stepsize = 0.28746 #full step
#stepsize = 0.071864 #quarter step
stepsize = 0.075    # 1/4 step
#stepsize = 0.035932  #eighth step

# one full step is about 0.29mm     #1391 steps ~ 400mm
# quarter step is about 0.072mm     #5566 steps ~ 400mm
# eighth step is 0.036mm            #11132 steps ~ 400mm
disTotal = 30 #(number of stops/cm)
disInterval = 5 #(mm) for each stop
stepTotal = disTotal*10/disInterval
resolution = 10
stepNum = int(disInterval/stepsize)
#############################################################################

#####################
## Motor driver setup
#####################

#### SPI SETUP ####
# chip select pin:
csp = 8
# clock speed in Hz:
cs = 3000000
# I think the motor driver can go up to 4MHz
# and the Adafruit board range is from 450hz to 30mhz
# SPI mode:
spiMode = 0
# Bit Order
bitOrder = 'MSB'

## Create HPSD object
sd = HighPowerStepperDriver.HighPowerStepperDriver()


sd.setupSPI(csp, cs, spiMode, bitOrder)

# give driver time to power up?
time.sleep(1)

#### MOTOR SETUP ####

# set decay mode: auto mixed decay recommended by documentation
sd.setDecayMode('AutoMixed')

## set current limit
sd.setCurrentLimit(current)

## set step mode
sd.setStepMode(stepMode)

## enable driver
sd.enableDriver()

    ######################
    # YEI IMU device setup
    ######################
    
    ## Timestamp mode
    ## 0 = sensor time
    ## 1 = system time
    ## 2 = none

#%%                           
## magnetometer data
dim = 2
restTime = 0.2
sleepT = 0.2
    
print('start!')
device = mag_data_py3.I2C_mag()

switch = digitalio.DigitalInOut(board.C1)
switch.direction = digitalio.Direction.OUTPUT

switch.value = False 
time.sleep(sleepT) 
envData = [device.all_data()]

switch.value = True   # switch on the power
time.sleep(sleepT)
magData = [device.all_data()]

effectMag = [magData[0][dim] - envData[0][dim]]
distance = [0]  
##############################################################################
# CHANGE THE STEP PATTERN HERE
##############################################################################
# setDirection()
# 0 = this moves platform toward timing pulley (toward motor)
# 1 = this moves platform toward to idler pulley (away from motor)

i = 1

for i in range(stepTotal -1):
    sd.step(stepNum,stepdelay)
    
    switch.value = False
    time.sleep(sleepT)
    envData.append(device.all_data())
    
    switch.value = True
    time.sleep(sleepT)
    magData.append(device.all_data())
    
    effectMag.append(magData[i][dim] - envData[i][dim])
    distance.append(distance[-1] + disInterval)
    i = i + 1
       
#############################
# Reset position back to 0
print("Resetting motor position.")
time.sleep(1)
sd.setDirection(0)
sd.step(stepNum*stepTotal,0.001)
    #############################
    
print("Saving data...")
# The stream data has parentheses and other formatting.
# This strips out the unwanted stuff
sd.disableDriver()

x = np.arange(stepTotal+1)
rawFile.write('\n'.join(str(x) for x in magData))
envFile.write('\n'.join(str(y) for y in envData))
#  disFile.write('\n'.join(str(z) for z in distance))
 
rawFile.close()
envFile.close()
#    disFile.close()

envZ = [column[dim] for column in envData]
plt.plot(x,effectMag,marker = 'o')
plt.savefig(filename+'N')
plt.figure()
plt.plot(x,envZ,marker = 'o')
plt.savefig(filename+'E')
plt.show()
    
#else:
    #print("No IMU devices found")
 
#%%       
name = [filename+ 'raw.txt',filename+ 'env.txt',filename+'distance.txt']
for filename in name:
    for line in fileinput.FileInput(filename, inplace=1):
        print(line.replace('[', '')),
        
    for line in fileinput.FileInput(filename, inplace=1):
        print(line.replace(']', '')),
        
    for line in fileinput.FileInput(filename, inplace=1):
        print(line.replace('(', '')),
        
    for line in fileinput.FileInput(filename, inplace=1):
        print(line.replace(')', '')),
        
    for line in fileinput.FileInput(filename, inplace=1):
        print(line.replace('))', '')),
                
    for line in fileinput.FileInput(filename, inplace=1):
        print(line.replace(',', '')),
            
    for line in fileinput.FileInput(filename, inplace=1):
        print(line.replace('L', '')),
