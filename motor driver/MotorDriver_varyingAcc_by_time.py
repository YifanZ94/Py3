# -*- coding: utf-8 -*-
"""
Created on Fri Mar  3 18:07:56 2023

@author: Administrator
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Mar  3 15:42:49 2023

@author: Administrator
"""

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

# reso = binaray(MS1,MS2)
reso = 1
# steps = round(disIncrement*135.47)
step_2_dist = 0.287   # 1 step = 0.287 mm


class motor:
    # def __init__(self):
        
    def move_one_step(self, step_delay): 
        step.value = True
        time.sleep(step_delay)
        step.value = False
        time.sleep(step_delay)
        
    def accelerate(self, current_delay, acc_times, Ts, direction):
        direc.value = direction
        # current_delay = min(t_max, current_delay)
        # target_delay = max(t_min, target_delay)
        # acc_times = round((current_delay - target_delay)/delay_change)
        step_count = 0
        for i in range(acc_times):
            T = round(current_delay -i*delay_change,4)
            steps_each_stage = round(Ts/T)
            step_count += steps_each_stage
            for j in range(steps_each_stage):
                self.move_one_step(T)
        return step_count
                
    def deaccelerate(self, current_delay, acc_times, Ts, direction):
        direc.value = direction
        # current_delay = max(t_min, current_delay)
        # target_delay = min(t_max, target_delay)
        # acc_times = round((current_delay - target_delay)/delay_change)
        step_count = 0
        for i in range(acc_times):
            T = round(current_delay +i*delay_change,4)
            steps_each_stage = round(Ts/T)
            step_count += steps_each_stage
            for j in range(steps_each_stage):
                self.move_one_step(T)
        return step_count

                 
# def random_move(distance):
    
Motor = motor()
direction = 1 # 1 is forward
Ts = 0.04


t_max = 4.5e-3
# t_max = 9.5e-3
t_min = 5e-4
# delay_change = (t_max - t_min)/acc_times
delay_change = 2e-4
enable.value = 0

min_steps = round(Ts/t_max)
max_steps = round(Ts/t_min)

#%% Forward by distance setting with nonlinear acc
# distance = 200
# steps = round(distance*reso/step_2_dist)
# step_count = 0
# stopLocations = []
# while step_count < steps:
#     acc_times = random.randint(10,20)
#     stopLocations.append(acc_times)
#     t_min_i = round(t_max - acc_times*delay_change, 4)
#     step_count += Motor.accelerate(t_max, acc_times, Ts, direction)
#     step_count += Motor.deaccelerate(t_min_i, acc_times, Ts, direction)
#     time.sleep(0.5)

# filename = input('enter the file name: ')       
# file = open(filename +'_stepperLocations.txt', 'w')
# np.savetxt(file, stopLocations)
# file.close()
# print('done')
# print(step_count)

#%%

T = []
for i in range(3):
    # constant acc
    max_speed_list = []
    max_speed_stpes = acc_times = random.randint(15,20)
    max_speed_list.append(max_speed_stpes)
    steps_per_increment = [1]
    for steps in range(1,max_speed_stpes):
        steps_per_increment.append(steps_per_increment[-1] + 1)
    for steps in range(1,max_speed_stpes):
        steps_per_increment.append(steps_per_increment[-1] - 1)    
    
    # linear varying acc
    # max_acc = random.randint(7,9)
    # steps_per_increment = [1]
    # for steps in range(1,max_acc):
    #     steps_per_increment.append(steps_per_increment[-1] + steps)
    # for steps in range(1, max_acc):
    #     steps_per_increment.append(steps_per_increment[-1] -max_acc +steps)    

    direc.value = direction
    for j in steps_per_increment:
        T.append(round(Ts/j,5))
        for i in range(j):
            Motor.move_one_step(T[-1])
    time.sleep(1)
    
    direc.value = 0
    for i in range(sum(steps_per_increment)):
        Motor.move_one_step(t_max)
    time.sleep(1)
    
enable.value = 1

# filename = input('enter the file name: ')       
# file = open(filename +'_maxSpeed.txt', 'w')
# np.savetxt(file, max_speed_list)
# file.close()



    
