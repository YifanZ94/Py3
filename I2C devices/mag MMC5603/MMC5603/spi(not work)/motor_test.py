# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 14:08:43 2020

@author: user
"""
import os
os.getcwd()
os.chdir('C:/Users/labuser/Desktop/py code/Python3/MMC5603')

import StepperDriver_py3
import time
#### SPI SETUP ####
# chip select pin:
csp = 8
# clock speed in Hz:
cs = 3000000

spiMode = 0
# Bit Order
bitOrder = 'MSB'

current = 2500
# stepper motor step size
stepMode = 'MicroStep4'
# stepper motor step delay
stepdelay = 0.001

## Create HPSD object
sd = StepperDriver_py3.HighPowerStepperDriver()

sd.setupSPI()
#sd.setupSPI(csp, cs, spiMode, bitOrder)
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
sd.setDirection(1)

sd.step(1000, stepdelay)

sd.disableDriver()