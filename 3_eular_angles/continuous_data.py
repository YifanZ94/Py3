import os
os.environ["BLINKA_FT232H"] = "1"  

import numpy as np
import board
import time 
import busio
import MMC5603
import mxc4005xc

import digitalio

i2c = board.I2C()
mag = MMC5603.Mag(i2c)
acc = mxc4005xc.MXC4005XC(i2c)

acc_list = []
mag_list = []
sleepT = 0.01

print('start')
time.sleep(0.1)
start = time.time()

last = 0
while last < 30:
    mag_list.append(mag.all_data())
    time.sleep(0.02)
    acc_list.append(acc.acceleration)
    time.sleep(0.02)
    last = time.time()-start
print('done')

filename = input('enter the file name ')
file = open(filename + '_mag.txt', 'w')
np.savetxt(file, np.array(mag_list))
file.close()

file = open(filename + '_acc.txt', 'w')
np.savetxt(file, np.array(acc_list))
file.close()