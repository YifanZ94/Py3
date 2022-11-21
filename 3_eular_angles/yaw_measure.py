import os
os.environ["BLINKA_FT232H"] = "1"  

import numpy as np
import board
import MMC5603
import mxc4005xc
from math import sin,cos,tan,atan,pi
import time 

i2c = board.I2C()
mag = MMC5603.Mag(i2c)
acc = mxc4005xc.MXC4005XC(i2c)

acc_list = []
angle_list = []
V = [0.092,0.052,0.11]

while True:
    try:
        time.sleep(1)
        print('press any key to continue')
        com = input()
        acc_reading = acc.acceleration
        angle = mxc4005xc.XY_angle(acc_reading[0],acc_reading[1],acc_reading[2])
        B_p = mag.all_data()
        B_fx = (B_p[0]-V[0])*cos(angle[1])+(B_p[1]-V[1])*sin(angle[0])*sin(angle[1])+(B_p[2]-V[2])*cos(angle[0])*sin(angle[1])
        B_fy = (B_p[1]-V[1])*cos(angle[0]) - (B_p[2]-V[2])*sin(angle[0])
        angle.append(atan(-B_fy/B_fx))
        angle_round = [round(i*180/pi,2) for i in angle]
        angle_list.append(angle_round)
        print(angle_round)
    except:
        print('done')
        break
        