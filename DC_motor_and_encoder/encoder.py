# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 11:42:29 2023

@author: Administrator
"""
import os 
os.environ["BLINKA_FT232H"] = "1"

import board
import time
import digitalio
import random 
import numpy as np

output1 = digitalio.DigitalInOut(board.C0)
output1.direction = digitalio.Direction.INPUT
output2 = digitalio.DigitalInOut(board.C1)
output2.direction = digitalio.Direction.INPUT
# relay = digitalio.DigitalInOut(board.C4)
# relay.direction = digitalio.Direction.OUTPUT

aLastState = output1.value
counter = 0
print('ready')
data = []
int_count = 0
start = time.time()

while True:
    try:
        # time.sleep(0.001)
        int_count += 1
        aState = output1.value
        if aState != aLastState:
            if output2.value != aState:
                counter += 1
                print(counter)  
                # data.append([counter, time.time()])
            else:
                counter -= 1
                print(counter)  
                # data.append([counter, time.time()])
            aLastState = aState
    except:
        break

print(time.time()-start)
# filename = input('enter the file name: ')       
# file = open(filename +'_encoder_count.txt', 'w')
# np.savetxt(file, np.array(data))
# file.close()

print('done')