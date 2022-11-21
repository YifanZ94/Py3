import numpy as np
import board
import time 
import busio
import MMC5603

i2c = board.I2C()
mag = MMC5603.Mag(i2c)
mag_list = []

import digitalio
relay = digitalio.DigitalInOut(board.D12)
relay.direction = digitalio.Direction.OUTPUT
relay.value = 0

com = 'y'
data = []
while com != 'n':
    relay.value = 1
    time.sleep(1)
    temp_data = []
    for i in range(2):
        temp_data.append(mag.all_data())
        time.sleep(0.02)
        
    relay.value = 0    
    I = input('enter the max current ')   
    ave_data = np.mean(temp_data,axis = 0) 
    ave_data = np.hstack((ave_data,float(I)))
    data.append(ave_data)
    
#     relay.value = 0
    
    com = input('any key to continue or n to quit  ')  

filename = input('enter the file name ')
file = open(filename + '_mag.txt', 'w')
np.savetxt(file, np.array(data))
file.close()