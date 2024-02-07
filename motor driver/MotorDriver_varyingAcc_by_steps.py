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
import os 
os.environ["BLINKA_FT232H"] = "1"

import board
import time
import digitalio
import random 
import numpy as np

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


# import board
# import time
# import digitalio
# import random 
# import numpy as np

# enable = digitalio.DigitalInOut(board.D17)
# enable.direction = digitalio.Direction.OUTPUT
# direc = digitalio.DigitalInOut(board.D23)
# direc.direction = digitalio.Direction.OUTPUT
# step = digitalio.DigitalInOut(board.D24)
# step.direction = digitalio.Direction.OUTPUT
# MS1 = digitalio.DigitalInOut(board.D5)
# MS1.direction = digitalio.Direction.OUTPUT
# MS2 = digitalio.DigitalInOut(board.D6)
# MS2.direction = digitalio.Direction.OUTPUT

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
        
    def accelerate(self, current_delay, target_delay, steps_total, direction):
        direc.value = direction
        current_delay = min(t_max, current_delay)
        target_delay = max(t_min, target_delay)
        acc_times = round((current_delay - target_delay)/delay_change)
        steps_each_stage = round(steps_total/acc_times)
        for i in range(acc_times):
            T = round(current_delay-i*delay_change,4)
            print(T)
            for j in range(steps_each_stage):
                self.move_one_step(T)
                
    def deaccelerate(self, current_delay, target_delay, steps_total, direction):
        direc.value = direction
        current_delay = max(t_min, current_delay)
        target_delay = min(t_max, target_delay)
        acc_times = round((current_delay - target_delay)/delay_change)
        steps_each_stage = round(steps_total/acc_times)
        for i in range(acc_times):
            T = round(current_delay+i*delay_change,4)
            print(T)
            for j in range(steps_each_stage):
                self.move_one_step(T)
        
                 
# def random_move(distance):
    
Motor = motor()
direction = 1     # 1 is forward  
distance = 100
steps = round(distance/step_2_dist)*10

delay_change = 2e-4
t_max = 4.5e-3
t_min = 5e-4
enable.value = 0

step_count = 0
current_delay = t_max
accelerated = 0


while step_count < steps:
    next_steps = random.randint(300,500)
    step_count += next_steps
    
    if accelerated == 0:
        t_min_i = round(t_min + random.randint(1,5)*delay_change,4)
        print('acc')
        Motor.accelerate(current_delay, t_min_i, next_steps, direction)
        accelerated = 1
        current_delay = t_min_i
        
    else:
        t_min_i = round(t_min + random.randint(15,19)*delay_change,4)
        print('de_acc')
        Motor.deaccelerate(current_delay, t_min_i, next_steps, direction)
        accelerated = 0
        current_delay = t_min_i
        time.sleep(0.4)


#%%
# for i in range(500):
#     Motor.move_one_step(t_min)

# next_steps = 2000
# Motor.accelerate(t_max, t_min, next_steps, direction)
# Motor.deaccelerate(t_min, t_max, next_steps, direction)

print('done')
enable.value = 1

    
