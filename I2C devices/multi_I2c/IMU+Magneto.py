# -*- coding: utf-8 -*-
"""
Created on Wed Dec 15 16:29:09 2021

@author: Administrator
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Dec 14 13:14:24 2021

@author: Administrator
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Mar 23 19:14:39 2021

@author: Administrator
"""
import time
import board
import busio 
import adafruit_lsm9ds0
import adafruit_lis2mdl
import numpy as np
import digitalio
i2c = busio.I2C(board.SCL, board.SDA)
IMU = adafruit_lsm9ds0.LSM9DS0_I2C(i2c)
MAG = adafruit_lis2mdl.LIS2MDL(i2c)

relay = digitalio.DigitalInOut(board.D12)
relay.direction = digitalio.Direction.OUTPUT

print('keep the sensor static then start calibration')
time.sleep(1)
sleepT = 0.01
acc_cali = []
gyro_cali = []
L = 20
for i in range(L):
    acc = IMU.acceleration
    gyro = IMU.gyro
    acc_cali.append(acc)
    gyro_cali.append(gyro)
    
gyro_bias = np.mean(np.array(gyro_cali),0)
acc_bias = np.mean(np.array(acc_cali),0)

def gyros():
    gyro_x, gyro_y, gyro_z = IMU.gyro
    return gyro_x-gyro_bias[0], gyro_y-gyro_bias[1], gyro_z-gyro_bias[2]
def acceleration():
    acc_x, acc_y, acc_z = IMU.acceleration
    return acc_x-acc_bias[0], acc_y-acc_bias[1], acc_z-(acc_bias[2]-9.81)
def measure(env_mag):
    acc_x, acc_y, acc_z = acceleration()
    gyro_x, gyro_y, gyro_z = gyros()
    mag_x, mag_y, mag_z = IMU.magnetic
    return [acc_x, acc_y, acc_z, gyro_x, gyro_y, gyro_z, mag_x-env_mag[0], mag_y-env_mag[1], mag_z-env_mag[2]]  # bias

def magnetometer_measure(env_mag):
    mag_x, mag_y, mag_z = MAG.magnetic
    return [mag_x-env_mag[0], mag_y-env_mag[1], mag_z-env_mag[2]] 

sleepT = 0.01
i = 0
s1_list = []
s2_list = []
print('start')
relay.value = 0
env_mag1 = IMU.magnetic
env_mag2 = MAG.magnetic
start = time.time()
relay.value = 1

while True:
    try:
        s1_list.append(measure(env_mag1))
        time.sleep(0.02)
        s2_list.append(magnetometer_measure(env_mag2))
        i += 1
        if i%10 == 0:
            relay.value = 0
            time.sleep(0.2)
            env_mag1 = IMU.magnetic
            env_mag2 = MAG.magnetic
            relay.value = 1
            time.sleep(0.2)
    except:
        break
    
duration = round(time.time() - start,2)

#%%
filename = input('enter the file name: ')       
file = open(filename +'IMU.txt', 'w')
np.savetxt(file, np.array(s1_list))
file.close()

file = open(filename +'Magneto.txt', 'w')
np.savetxt(file, np.array(s2_list))
file.close()