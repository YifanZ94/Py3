# Simple demo of the LSM9DS1 accelerometer, magnetometer, gyroscope.
# Will print the acceleration, magnetometer, and gyroscope values every second.
import os 
os.environ["BLINKA_FT232H"] = "1" 

import time
import board
import busio
import adafruit_lsm9ds1
import numpy as np

# I2C connection:
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_lsm9ds1.LSM9DS1_I2C(i2c)

# print('calibration start')
# calib = []
# for i in range(20):
#     accel_x, accel_y, accel_z = sensor.acceleration
#     calib.append([accel_x, accel_y, accel_z])
#     time.sleep(0.1)    
# bias = np.mean(np.array(calib), axis=0)    
    
print('test start')
start = time.time()
data = []

while True:
    command = input('n to stop collect data ')
    if command != 'n':
    # Read acceleration, magnetometer, gyroscope, temperature.
        accel_x, accel_y, accel_z = sensor.acceleration
        gyro_x, gyro_y, gyro_z = sensor.gyro
        # acc.append([accel_x-bias[0], accel_y-bias[1], accel_z])
        data.append([accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z])
        # time.sleep(0.01)
    else:
        break
    
# duration = time.time() - start
# print(duration)
filename = input('enter the file name: ')       
file = open(filename + '_acc.txt', 'w')
np.savetxt(file, np.array(data))
file.close()    

import matplotlib.pyplot as plt
plt.plot(np.array(data)[:,1])
plt.show()
    
