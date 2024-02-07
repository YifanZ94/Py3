# -*- coding: utf-8 -*-
"""
Created on Tue Mar 23 19:14:39 2021

@author: Administrator
"""

import os 
os.environ["BLINKA_FT232H"] = "1" 
# os.chdir('F:\py code\Py3\I2C devices\IMU_LSM9DS0')

import time
import board
import busio 
import adafruit_lsm9ds0
import numpy as np
from math import atan, atan2, sin, cos, pi
from numpy.linalg import inv, norm
# I2C connection:
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_lsm9ds0.LSM9DS0_I2C(i2c)

#%% calibration for bias and time interval
# def atanp(x,y):
#     angle = atan2(x,y)
#     if angle < 0:
#         angle += pi
#     return angle

print('keep the sensor static then start calibration')
time.sleep(1)
sleepT = 0.01
acc_cali = []
gyro_cali = []
L = 20
for i in range(L):
    acc = sensor.acceleration
    gyro = sensor.gyro
    acc_cali.append(acc)
    gyro_cali.append(gyro)
    
gyro_bias = np.mean(np.array(gyro_cali),0)
acc_bias = np.mean(np.array(acc_cali),0)
mag_ref = sensor.magnetic
yaw_ref = atan2(-mag_ref[1],mag_ref[0])
# gyro_bias = np.array([0,0,0])
# acc_bias = np.array([0,0,0])

def gyros():
    gyro_x, gyro_y, gyro_z = sensor.gyro
    return [gyro_x-gyro_bias[0], gyro_y-gyro_bias[1], gyro_z-gyro_bias[2]]
def acceleration():
    acc_x, acc_y, acc_z = sensor.acceleration
    return [acc_x-acc_bias[0], acc_y-acc_bias[1], acc_z-(acc_bias[2]-9.81)]
def magnetic():
    mag_x, mag_y, mag_z = sensor.magnetic
    return [mag_x, mag_y, mag_z]
def rotX(roll):
    np.array([(1,0,0),(0,cos(roll),-sin(roll)),(0,sin(roll),cos(roll))])
def rotY(pitch):
    np.array([(cos(pitch),0,sin(pitch)),(0,1,0),(-sin(pitch),0,cos(pitch))])
def rotZ(yaw):
    np.array([(cos(yaw),sin(yaw),0),(-sin(yaw),cos(yaw),0),(0,0,1)])
#%%  complimentary filtering for attitude
roll_gyro = 0
pitch_gyro = 0
yaw_gyro = 0

alpha = 0.1

angles_comp = []
angles_acc = []
angles_gyro = []
print('start measuring')
measure_L = 500
acc_threshold = 9.9
gyro_threshold = 0.1
yaw_mag = 0
for i in range(measure_L):
    t1 = time.time()
    acc = acceleration()
    gyro = gyros()
    mag = magnetic()
    t2 = time.time()
    T_int = t2-t1
    
    roll_acc = atan2(acc[1], acc[2])
    pitch_acc = atan(-acc[0]/(sin(acc[1])+cos(acc[2])))
    roll_gyro += T_int*gyro[0]*pi/180
    pitch_gyro += T_int*gyro[1]*pi/180
    yaw_gyro += T_int*gyro[2]*pi/180
    
    roll_comp = alpha*roll_acc+(1-alpha)*roll_gyro
    pitch_comp = alpha*pitch_acc+(1-alpha)*pitch_gyro
    
    if norm(acc)>acc_threshold or norm(gyro)>gyro_threshold:
        yaw_mag = atan2((mag[2]*sin(roll_comp)-mag[1]*cos(roll_comp)), 
                       (mag[0]*cos(pitch_comp) + mag[1]*sin(roll_comp)*sin(pitch_comp) 
                        + mag[2]*sin(pitch_comp)*cos(roll_comp))) - yaw_ref
        
    beta = 0.1
    yaw_comp = beta*yaw_mag + (1-beta)*yaw_gyro
    
    angles_acc.append([roll_acc,pitch_acc,yaw_mag])
    angles_gyro.append([roll_gyro,pitch_gyro,yaw_gyro])
    angles_comp.append([roll_comp, pitch_comp, yaw_comp])
    
print('done') 

import matplotlib.pyplot as plt
x = np.arange(measure_L)
plt.plot(x,np.array(angles_acc)[:,0],x,np.array(angles_gyro)[:,0],x,np.array(angles_comp)[:,0])
plt.legend(['acc', 'gyro', 'comp'])
plt.title('roll(rad)')
plt.show()
plt.plot(x,np.array(angles_acc)[:,1],x,np.array(angles_gyro)[:,1],x,np.array(angles_comp)[:,1])
plt.legend(['acc', 'gyro', 'comp'])
plt.title('pitch(rad)')
plt.show()
plt.plot(x,np.array(angles_acc)[:,2],x,np.array(angles_gyro)[:,2],x,np.array(angles_comp)[:,2])
plt.legend(['mag', 'gyro', 'comp'])
plt.title('yaw(rad)')
plt.show()   
# end = time.time()
# filename = input('enter the file name: ')       
# file = open(filename + str(round(end-start,2)) + '_AngleComp.txt', 'w')
# np.savetxt(file, np.array(angles))
# file.close()
