# -*- coding: utf-8 -*-
"""
Created on Tue Jan 23 16:59:24 2024

@author: Administrator
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Jan 16 13:22:48 2024

@author: Administrator
"""
# SPDX-FileCopyrightText: 2020 Dan Halbert for Adafruit Industries
#
# SPDX-License-Identifier: MIT

# Connect to an "eval()" service over BLE UART.
import time 
import struct
import numpy as np

from adafruit_ble import BLERadio, BLEConnection
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService

ble = BLERadio()

uart_connection = None
s = str(1)
data_list = []
idx = 0

#%%

while True:
    try:
        if not uart_connection:
            print("Trying to connect...")
            for adv in ble.start_scan(ProvideServicesAdvertisement):
                if UARTService in adv.services:
                    uart_connection = ble.connect(adv)
                    print("Connected")
                    start = time.time()
                    break
            ble.stop_scan()
        
        if uart_connection and uart_connection.connected:
            uart_service = uart_connection[UARTService]
            uart_service.connection_interval = 2.5
            
            while uart_connection.connected:
                try:
                    # uart_service.write(s.encode("utf-8"))
                    uart_service.write(b's')
                    uart_service.write(b'\n')
                    
                    # data = uart_service.readline().decode("utf-8")
                    
                    a = uart_service.readline()
                    data = struct.unpack('6fs', a)
                    # print(data)
                    data_list.append(np.array(data[0:6]))
                    
                except Exception as e:
                    idx += 1
                    print(Exception)
                    
    except:
        end = time.time()
        uart_connection.disconnect()
        break

#%%        
Ts = (end - start)/len(data_list)

import matplotlib.pyplot as plt
data_plot = np.array(data_list)
x = np.arange(data_plot.shape[0])
plt.plot(x,data_plot[:,2])
plt.show()