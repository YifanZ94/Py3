# -*- coding: utf-8 -*-
"""
Find sensors and print out i2c address
"""

import os
os.environ["BLINKA_MCP2221"] = "1"
# os.environ["BLINKA_FT232H"] = "1"

import board

i2c = board.I2C()  # uses board.SCL and board.SDA

while not i2c.try_lock():
    pass

# Print the addresses found
print("I2C addresses found:", [hex(device_address)
                               for device_address in i2c.scan()])

i2c.unlock()
