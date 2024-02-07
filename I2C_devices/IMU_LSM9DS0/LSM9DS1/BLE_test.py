# -*- coding: utf-8 -*-
"""
Created on Tue Jan 30 13:30:14 2024

@author: Administrator
"""

# Simple demo of the LSM9DS1 accelerometer, magnetometer, gyroscope.
# Will print the acceleration, magnetometer, and gyroscope values every second.
import time
import board
import busio
import adafruit_lsm9ds1

# I2C connection:
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_lsm9ds1.LSM9DS1_I2C(i2c)
ACCELRANGE_2G = 0b00 << 3
ACCELRANGE_16G = 0b01 << 3
ACCELRANGE_4G = 0b10 << 3
ACCELRANGE_8G = 0b11 << 3
MAGGAIN_4GAUSS = 0b00 << 5  # +/- 4 gauss
MAGGAIN_8GAUSS = 0b01 << 5  # +/- 8 gauss
MAGGAIN_12GAUSS = 0b10 << 5  # +/- 12 gauss
MAGGAIN_16GAUSS = 0b11 << 5  # +/- 16 gauss
GYROSCALE_245DPS = 0b00 << 3  # +/- 245 degrees/s rotation
GYROSCALE_500DPS = 0b01 << 3  # +/- 500 degrees/s rotation
GYROSCALE_2000DPS = 0b11 << 3  # +/- 2000 degrees/s rotation

sensor.accel_range = ACCELRANGE_4G

print('test start')
start = time.time()
data = []

while True:
    try:
    # changed from left hand coord to right hand coord
        accel_x, accel_y, accel_z = sensor.acceleration
        gyro_x, gyro_y, gyro_z = sensor.gyro
        mag_x, mag_y, mag_z = sensor.magnetic
        print([accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z, mag_x, mag_y, mag_z])
        time.sleep(0.2)
        
    except:
        break
    
duration = time.time() - start
print(duration)
    

