# -*- coding: utf-8 -*-
"""
Created on Mon Feb 15 14:07:53 2021

@author: Administrator
"""
# import os 
# os.environ["BLINKA_FT232H"] = "1"

import board
import time
import digitalio
import random 
import numpy as np
import multiprocessing as mp
import adafruit_lsm9ds0

# enable = digitalio.DigitalInOut(board.C0)
# enable.direction = digitalio.Direction.OUTPUT
# direc = digitalio.DigitalInOut(board.C2)
# direc.direction = digitalio.Direction.OUTPUT
# step = digitalio.DigitalInOut(board.C1)
# step.direction = digitalio.Direction.OUTPUT
# MS1 = digitalio.DigitalInOut(board.D6)
# MS1.direction = digitalio.Direction.OUTPUT
# MS2 = digitalio.DigitalInOut(board.D7)
# MS2.direction = digitalio.Direction.OUTPUT

enable = digitalio.DigitalInOut(board.D17)
enable.direction = digitalio.Direction.OUTPUT
direc = digitalio.DigitalInOut(board.D23)
direc.direction = digitalio.Direction.OUTPUT
step = digitalio.DigitalInOut(board.D24)
step.direction = digitalio.Direction.OUTPUT
MS1 = digitalio.DigitalInOut(board.D5)
MS1.direction = digitalio.Direction.OUTPUT
MS2 = digitalio.DigitalInOut(board.D6)
MS2.direction = digitalio.Direction.OUTPUT

MS1.value = 0
MS2.value = 0

i2c = board.I2C()
IMU = adafruit_lsm9ds0.LSM9DS0_I2C(i2c)
for i in range(10):
    IMU.acceleration
    IMU.gyro
    time.sleep(0.1)

step_2_dist = 0.287   # 1 step = 0.287 mm

class motor:
    # def __init__(self):
        
    def move_one_step(self, step_delay): 
        step.value = True
        time.sleep(step_delay)
        step.value = False
        time.sleep(step_delay)
                 
def fun1(q,inc_time,max_speed,test_num):
    
    IMU_data = np.hstack((np.array([IMU.acceleration]),np.array([IMU.gyro])))
    for i in range(10):
        IMU_data = np.vstack((IMU_data, np.hstack((np.array([IMU.acceleration]),np.array([IMU.gyro])))))
        time.sleep(0.1)
    IMU_bias = np.mean(IMU_data, axis=0)
    IMU_bias[2] = IMU_bias[2] - 9.81
#     print('the bias is ' + str(IMU_bias))
    IMU_data = np.hstack((np.array([IMU.acceleration]),np.array([IMU.gyro]))) - IMU_bias
#     print('the first reading is ' + str(IMU_data))
    
    speed_str = str(max_speed.value)
    T_c_str = str(inc_time.value)
    
    q.put(1)
    start = time.time()
    print('IMU start time ' + str(start))
    while True:
        if q.empty():
            IMU_data = np.vstack((IMU_data, np.hstack((np.array([IMU.acceleration]),np.array([IMU.gyro])))-IMU_bias))
            time.sleep(0.01)
        else:
            if q.get() == 0:
                break
#     print('finish collecting data')
    end = time.time()
    print('IMU end time ' + str(end))
    time_all = str(round(end-start, 2))
    print('IMU stream duration ' + str(time_all))
    
    file = open('test'+str(test_num)+'_Tc'+T_c_str + '_maxSpeed'+ speed_str +'_T'+ time_all +'.txt','w')
    np.savetxt(file, IMU_data)
    file.close()
    
#     import matplotlib.pyplot as plt
#     x = np.arange(len(IMU_data))
#     plt.plot(x,IMU_data[:,0])
#     plt.show()
#     print('p1 done')

            
def fun2(q,inc_time,max_speed):
    Motor = motor()
    direction = 1    # 1 is forward  
    Ts0 = 0.010
    Ts = Ts0 + random.randint(0,4) * 0.005
    max_speed_stpes = random.randint(20,30)
    inc_time.value = Ts
    max_speed.value = max_speed_stpes

    steps_per_increment = [1]
    for steps in range(1,max_speed_stpes):
        steps_per_increment.append(steps_per_increment[-1] + 1)
    for steps in range(1,max_speed_stpes):
        steps_per_increment.append(steps_per_increment[-1] - 1) 
    T = []
    
    while True:
        if q.get() == 1:
            start = time.time()
            print('Motor start time ' + str(start))
            enable.value = 0
            direc.value = direction
            for j in steps_per_increment:
                delay_i = max(round(Ts/j,5), 5e-4)
                T.append(delay_i)
                for i in range(j):
                    Motor.move_one_step(T[-1])
            q.put(0)
            end = time.time()
            print('Motor end time ' + str(end))
            time_all = str(round(end-start, 2))
            print('Motor moving duration ' + str(time_all))
            time.sleep(1)
            break
        
    direc.value = not direction
    for i in range(sum(steps_per_increment)):
        Motor.move_one_step(2e-3)
    time.sleep(1)    
    enable.value = 1
    print('p2 done')
        
        
q = mp.Queue()    # start and stop comman
inc_time = mp.Value('d', 0.0)
max_speed = mp.Value('i', 0)

for test_num in range(1,2):
    p1 = mp.Process(target=fun1, args=(q,inc_time,max_speed,test_num,))
    p2 = mp.Process(target=fun2, args=(q,inc_time,max_speed,))
    
    p1.start()
    p2.start()
    
    p1.join()
    p2.join()
    
    print('both finished')
    time.sleep(0.5)
    
