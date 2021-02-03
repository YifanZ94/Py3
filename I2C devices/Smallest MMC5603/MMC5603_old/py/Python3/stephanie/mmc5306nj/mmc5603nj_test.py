# -*- coding: utf-8 -*-
"""
Created on Wed Jul  1 09:56:08 2020

@author: Stephanie

based off example from lis2mdl simpletest code
"""

""" Display magnetometer data once per second """

import time
import board
import busio
import driver_mmc5603NJ

i2c = busio.I2C(board.SCL, board.SDA)
sensor = driver_mmc5603NJ.MMC5603NJ(i2c)

## RESET
## reset the sensor?
# sensor.reset()


## SINGLE MEASUREMENT
## take single magnetic measurement
## buggy, weird numbers?
magx, magy, magz = sensor.magnetic_single
print("X:{0:7.2f}, Y:{1:7.2f}, Z:{2:7.2f} ".format(magx, magy, magz))

## take single magnetic measurement periodically
## buggy, weird numbers?
# while True:
#     magx, magy, magz = sensor.magnetic_single
#     print("X:{0:7.2f}, Y:{1:7.2f}, Z:{2:7.2f} ".format(magx, magy, magz))
#     time.sleep(0.1)

## print raw
# while True:
#     mag_x0, mag_x1, mag_x2, mag_y0, mag_y1, mag_y2, mag_z0, mag_z1, mag_z2 = sensor.magnetic_raw
#     print("X0: {0:08b}, X1: {1:08b}, X2: {2:08b} ".format(mag_x0, mag_x1, mag_x2))
#     print("Y0: {0:08b}, Y1: {1:08b}, Y2: {2:08b} ".format(mag_y0, mag_y1, mag_y2))
#     print("Z0: {0:08b}, Z1: {1:08b}, Z2: {2:08b} ".format(mag_z0, mag_z1, mag_z2))
#     time.sleep(1)

## CONTINUOUS
## this doesn't work yet
# sensor.magnetic_cmm()


## TEMPERATURE
## temperature measurement
# degree_sign= u'\N{DEGREE SIGN}'
# temp = sensor.temperature
# print("temp: {:5.2f}".format(temp)+degree_sign+"C")