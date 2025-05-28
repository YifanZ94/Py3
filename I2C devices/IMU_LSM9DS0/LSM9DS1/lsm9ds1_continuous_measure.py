# Simple demo of the LSM9DS1 accelerometer, magnetometer, gyroscope.
# Will print the acceleration, magnetometer, and gyroscope values every second.
import os 
os.environ["BLINKA_FT232H"] = "1" 
# os.environ["BLINKA_MCP2221"] = "1"

import time
import board
import busio
import adafruit_lsm9ds1
import numpy as np

# I2C connection:
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_lsm9ds1.LSM9DS1_I2C(i2c)
gyro_x, gyro_y, gyro_z = sensor.gyro
time.sleep(3)

print('calibration start')
calib = []
for i in range(20):
    # accel_x, accel_y, accel_z = sensor.acceleration
    # calib.append([accel_x, accel_y, accel_z])
    # time.sleep(0.1)    
    gyro_x, gyro_y, gyro_z = sensor.gyro
    calib.append([gyro_x, gyro_y, gyro_z])
    time.sleep(0.1)  
bias = np.mean(np.array(calib), axis=0)    
    
print('test start')
start = time.time()
data = []
acc = []
gyro = []
while True:
    try:
    # changed from left hand coord to right hand coord
        accel_x, accel_y, accel_z = sensor.acceleration
        gyro_x, gyro_y, gyro_z = sensor.gyro
        mag_x, mag_y, mag_z = sensor.magnetic
        data.append([accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z, mag_x, mag_y, mag_z])
        # acc.append([accel_x, accel_y, accel_z])
        # gyro.append([gyro_x - bias[0], gyro_y- bias[1], gyro_z- bias[2]])
        
    except:
        break
    
duration = time.time() - start
print(duration)
filename = input('enter the file name: ')     
file = open(filename + '_IMU.txt', 'w')
np.savetxt(file, np.array(data))
file.close()   
  
# file = open('acc_raw.txt', 'w')
# np.savetxt(file, np.array(acc))
# file.close()    

# file = open('gyro.txt', 'w')
# np.savetxt(file, np.array(gyro))
# file.close()    

#%%
import matplotlib.pyplot as plt
plt.plot(np.array(data)[:,3:6])
plt.show()
    
