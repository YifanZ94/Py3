# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 19:34:13 2020

@author: Administrator
"""

import os 
os.environ["BLINKA_FT232H"] = "1"

import time
import board
import busio

i2c = busio.I2C(board.SCL, board.SDA)
address = 0x30

"""
read from address, register 'byte'
"""  
#
def gauss(data):
    r = data[0] << 8 | data[1]
    Gauss = (r/(65536.0) - 0.5)*60.0
    
    return Gauss

while True:
    i2c.try_lock()
    i2c.writeto(address, bytes([0x1b,1]), stop=False)
    i2c.writeto(address, bytes([0x00,0x01]), stop=False)
    result = bytearray(2)
    i2c.readfrom_into(address,result)
    print(gauss(result))
    i2c.unlock()
    time.sleep(0.2)
