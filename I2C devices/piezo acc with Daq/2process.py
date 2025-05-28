# -*- coding: utf-8 -*-
"""
Created on Thu Nov 17 19:16:00 2022

@author: Administrator
"""

#%%
import os 
os.environ["BLINKA_FT232H"] = "1" 

import multiprocessing
import time
import numpy as np
import adafruit_lsm9ds1
import board
import digitalio
import busio
import nidaqmx

i2c = busio.I2C(board.SCL, board.SDA)
IMU = adafruit_lsm9ds1.LSM9DS1_I2C(i2c)
task = nidaqmx.Task()
task.ai_channels.add_ai_voltage_chan("Dev4/ai0")
filename = input('enter the file name: ')      

#%%
def func1(q):
    acc = []
    while True:
        if q.empty():
            accel_x, accel_y, accel_z = IMU.acceleration
            acc.append([accel_x, accel_y, accel_z])
        else:
            command = q.get()
            if command ==0:
                print('stop in p1')
                q.put(0)
                break   
        
    ## saving text not working
    # file = open(filename +'_IMU.txt', 'w')
    # np.savetxt(file, np.array(acc))
    # file.close()
        
#%%  
def func2(q,background_mag):  
    piezo = []
    while True:
        if q.empty():
            piezo.append(task.read())
            
        else:
            command = q.get()
            if command == 0:
                print('stop in p2')
                q.put(0)
                break
            
    # file = open(filename +'_piezo.txt', 'w')
    # np.savetxt(file, np.array(piezo))
    # file.close()
    
#%%  main
q = multiprocessing.Queue()
p1 = multiprocessing.Process(target=func1, args=(q,)) 
p2 = multiprocessing.Process(target=func2, args=(q,)) 
p1.start()
p2.start()

while True:
    try:
#         print('waiting in main loop')
        time.sleep(0.2)
        pass
    except:
        q.put(0)
        p2.join() 
        p1.join()
        break

print("Done!") 