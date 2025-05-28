import os 
os.environ["BLINKA_FT232H"] = "1"         # different microcontroller

import board
import time 
import busio

deviceAdd = 0x30
identi_addr = 0x39
inter_control = 0x1b
control2 = 0x1c
X_H_add = 0x00

class Mag:
    
    def __init__(self,bus):
        self.i2c = bus
        self.i2c.writeto(deviceAdd, bytes([control2,0b10000000]))
        for i in range(10):
            self.all_data()
        
    def all_data(self):
#         self.i2c.writeto(deviceAdd, bytes([inter_control,0b00110001]))
        self.i2c.writeto(deviceAdd, bytes([inter_control,0b00100001]))
        time.sleep(0.02)
        self.Wbuffer = bytes([X_H_add])
        self.Rbuffer = bytearray(6)
        self.i2c.writeto_then_readfrom(deviceAdd,self.Wbuffer, self.Rbuffer)
        self.Xbyte2long = self.Rbuffer[0] << 8 | self.Rbuffer[1]
        self.Ybyte2long = self.Rbuffer[2] << 8 | self.Rbuffer[3]
        self.Zbyte2long = self.Rbuffer[4] << 8 | self.Rbuffer[5]
        self.Xgauss = (self.Xbyte2long/65536.0 - 0.5)*60
        self.Ygauss = (self.Ybyte2long/65536.0 - 0.5)*60
        self.Zgauss = (self.Zbyte2long/65536.0 - 0.5)*60
        return [self.Xgauss,self.Ygauss,self.Zgauss]
    
#     
# import time
# i2c = board.I2C()
# mag = Mag(i2c)
# print('ready to go')
# ans = []
# start = time.time()

# while True:
#     try:
#         ans.append(mag.all_data())
#         time.sleep(0.01)
#     except OSError:
#         break

# end = time.time()
# print(end-start)    
# import numpy as np
# import matplotlib.pyplot as plt
# x = np.arange(len(ans))
# magData = np.array(ans)
# plt.plot(x,magData)
# plt.show()


# filename = input('enter the file name ')
# file = open(filename + '_mag.txt', 'w')
# np.savetxt(file, np.array(ans))
# file.close()