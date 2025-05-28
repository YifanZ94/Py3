

import os 
os.environ["BLINKA_FT232H"] = "1" 

import time
import board
import busio 
import adafruit_lsm9ds0
import numpy as np
import digitalio
import matplotlib.pyplot as plt

i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_lsm9ds0.LSM9DS0_I2C(i2c)
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
    time.sleep(0.05)
    
gyro_bias = np.mean(np.array(gyro_cali),0)
acc_bias = np.mean(np.array(acc_cali),0)
mag_ref = sensor.magnetic

def gyros():
    gyro_x, gyro_y, gyro_z = sensor.gyro
    return gyro_x-gyro_bias[0], gyro_y-gyro_bias[1], gyro_z-gyro_bias[2]
def acceleration():
    acc_x, acc_y, acc_z = sensor.acceleration
    return acc_x-acc_bias[0], acc_y-acc_bias[1], acc_z-(acc_bias[2]-9.81)
def magnetic():
    mag_x, mag_y, mag_z = sensor.magnetic
    return mag_x, mag_y, mag_z

def measure():
    # acc_x, acc_y, acc_z = acceleration()
    # gyro_x, gyro_y, gyro_z = gyros()
    mag_x, mag_y, mag_z = magnetic()
    # acc_x, acc_y, acc_z, gyro_x, gyro_y, gyro_z,
    return [ mag_x, mag_y, mag_z]  # bias

print('start')
start = time.time()
s1_list = []
time.sleep(2)
while True:
    try:
        s1_list.append(measure())
        time.sleep(0.01)
    except:
        break
duration = round(time.time() - start,2)
s1_array = np.array(s1_list)

#%% plot mag X
x = np.arange(len(s1_list))
npData = np.array(s1_list)
y = npData[:,1]
plt.plot(x,y)
plt.show()

#%%
print(duration)
filename = input('enter the file name: ')       
file = open(filename +'_lsm9ds0.txt', 'w')
np.savetxt(file, np.array(s1_array))
file.close()