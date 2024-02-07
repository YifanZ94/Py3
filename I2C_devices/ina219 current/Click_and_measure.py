# Simple demo of the LSM9DS1 accelerometer, magnetometer, gyroscope.
# Will print the acceleration, magnetometer, and gyroscope values every second.
import os 
os.environ["BLINKA_FT232H"] = "1" 

import time
import board
import busio
import adafruit_lsm9ds0
from adafruit_ina219 import ADCResolution, BusVoltageRange, INA219
import numpy as np

# I2C connection:
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_lsm9ds0.LSM9DS0_I2C(i2c)
ina219 = INA219(i2c)
ina219.bus_adc_resolution = ADCResolution.ADCRES_12BIT_32S
ina219.shunt_adc_resolution = ADCResolution.ADCRES_12BIT_32S
    
print('test start')
start = time.time()
data = []

while True:
    command = input('n to stop collect data ')
    if command != 'n':
    # Read acceleration, magnetometer, gyroscope, temperature.
        # accel_x, accel_y, accel_z = sensor.acceleration
        # gyro_x, gyro_y, gyro_z = sensor.gyro
        
        mag_x, mag_y, mag_z = sensor.magnetic
        current = ina219.current
        data.append([mag_x, mag_y, mag_z, current])
        
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
    
