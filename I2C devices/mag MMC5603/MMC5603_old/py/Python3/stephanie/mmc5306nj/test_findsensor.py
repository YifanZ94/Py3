# -*- coding: utf-8 -*-
"""
Created on Wed Jun 24 16:19:04 2020

@author: Stephanie
"""

# Step 1: Find Your Sensor
# Do an I2C scan to see if board is detected, and 
# if it is, print out its I2C address


#import time

import board
import busio

i2c = busio.I2C(board.SCL, board.SDA)


# Lock the I2C device before we try to scan
while not i2c.try_lock():
    pass

# Print the addresses found once
print("I2C addresses found:", [hex(device_address)
                               for device_address in i2c.scan()])

# Unlock I2C now that we're done scanning.
i2c.unlock()