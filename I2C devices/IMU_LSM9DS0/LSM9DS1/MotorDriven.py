# -*- coding: utf-8 -*-
"""
Created on Mon Feb 15 14:07:53 2021

@author: Administrator
"""
import os 
# os.environ["BLINKA_MCP2221"] = "1"
os.environ["BLINKA_FT232H"] = "1"         # different microcontroller

import board
import time
import digitalio
import numpy as np
import multiprocessing as mp
import adafruit_lsm9ds1
import busio

enable = digitalio.DigitalInOut(board.C0)
enable.direction = digitalio.Direction.OUTPUT
direc = digitalio.DigitalInOut(board.C2)
direc.direction = digitalio.Direction.OUTPUT
step = digitalio.DigitalInOut(board.C1)
step.direction = digitalio.Direction.OUTPUT
MS1 = digitalio.DigitalInOut(board.D6)
MS1.direction = digitalio.Direction.OUTPUT
MS2 = digitalio.DigitalInOut(board.D7)
MS2.direction = digitalio.Direction.OUTPUT

MS1.value = False
MS2.value = False

class motor:
    def __init__(self):
        self.stepdelay = 5e-3
        enable.value = False
        # MS1.value = False
        # MS2.value = True
        
    def move_one_step(self,dirIn): 
        if dirIn == 0:
            direc.value = True
        else:
            direc.value = False
        step.value = True
        time.sleep(self.stepdelay)
        step.value = False
        time.sleep(self.stepdelay)
        
    def move(self,dist,dirIn): 
        if dirIn == 0:
            direc.value = True
        else:
            direc.value = False
        enable.value = False

        self.steps = round(dist*3*250/5.3)
        for i in range(self.steps):
            step.value = True
            time.sleep(self.stepdelay)
            step.value = False
            time.sleep(self.stepdelay)
        enable.value = True
        
    def reset(self):
        enable.value = True

angle_target = [10,20,-10,-20]
angle_delta = [angle_target[0]]
for i in range(1,len(angle_target)):
    angle_delta.append(angle_target[i]-angle_target[i-1])

def fun1(q,inc_time,max_speed,test_num):
    i2c = busio.I2C(board.SCL, board.SDA)
    sensor = adafruit_lsm9ds1.LSM9DS1_I2C(i2c)
    acc_data = []
    gyro_data = []
    for i in range(10):
        accel_x, accel_y, accel_z = sensor.acceleration
        gyro_x, gyro_y, gyro_z = sensor.gyro
        acc_data.append([accel_x, accel_y, accel_z])
        gyro_data.append([ gyro_x, gyro_y, gyro_z])
    
    start = time.time()
    while True:
        if q.empty():
            gyro_x, gyro_y, gyro_z = sensor.gyro
            gyro_data.append([ gyro_x, gyro_y, gyro_z])
        else:
            if q.get() == 0:
                break
            elif q.get() == 1:
                accel_x, accel_y, accel_z = sensor.acceleration
                acc_data.append([accel_x, accel_y, accel_z])
#     print('finish collecting data')
    end = time.time()
    time_all = str(round(end-start, 2))
    print('IMU stream duration ' + str(time_all))
    
    file = open('T'+ str(time_all) +'_gyro.txt','w')
    np.savetxt(file, np.array(gyro_data))
    file.close()
    file = open('T'+ str(time_all) +'_acc.txt','w')
    np.savetxt(file, np.array(acc_data))
    file.close()
    
            
def fun2(q,inc_time,max_speed):
    Motor = motor()
    direction = 1    # 1 is forward  
    for angle in angle_delta:
        q.put(1)
        time.sleep(0.2)
        steps = round(angle/0.9)
        for s in range(steps):
            Motor.move_one_step(direction)
        q.put(1)
        time.sleep(0.2)
        Motor.reset()
    q.put(0)
            

q = mp.Queue() 
p1 = mp.Process(target=fun1, args=(q,))
p2 = mp.Process(target=fun2, args=(q,))

p1.start()
p2.start()

p1.join()
p2.join()

print('both finished')
    