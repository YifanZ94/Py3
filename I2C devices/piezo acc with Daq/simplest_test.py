# -*- coding: utf-8 -*-
"""
Created on Thu Nov 17 17:53:36 2022

@author: Administrator
"""

import nidaqmx
import time
data = []
start = time.time()
task = nidaqmx.Task()
task.ai_channels.add_ai_voltage_chan("Dev4/ai0")
time1 = time.time()
print(time1-start)

for i in range(1000):
    data.append(task.read())

time2 = time.time()
print(time2-time1)