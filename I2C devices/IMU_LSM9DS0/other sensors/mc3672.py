# -*- coding: utf-8 -*-
"""
Created on Thu Jan  7 15:19:31 2021

@author: Administrator
"""
import os 
os.environ["BLINKA_FT232H"] = "1" 

import board
import time 
import math
import numpy as np
# register map
# read only
X_DATA0 = 0x02
X_DATA1 = 0x03
Y_DATA0 = 0x04
Y_DATA1 = 0x05
Z_DATA0 = 0x06
Z_DATA1 = 0x07

status = 0x08
status2 = 0x01

# write 
deviceAdd = 0x4C
control = 0x10
RangeAndReso = 0x15
feature = 0x0D
InitReg1 = 0x0F
InitReg2 = 0x28
InitReg3 = 0x1A
X_motion = 0x20
Y_motion = 0x21
Z_motion = 0x22
Trig_count = 0x29
reset = 0x24
scratch_pad = 0x1B

# buffer = bytes([X_DATA0,X_DATA1,Y_DATA0,Y_DATA1,Z_DATA0,Z_DATA1])

# change from 2's complement
def unsign2signG(unsign):
    ordi = 8
    if unsign < 2**(ordi-1):
        signed = unsign
    else:
        unsign &= 0b0000000011111111
        signed = -(2**ordi - unsign)
                   
    return (signed/2**(ordi-1))*19.614

def rotMatrix(accX,accY,accZ):
    Ax = math.atan(-accY/accZ)
    Ay = -math.atan(-accX/(math.sqrt(accY**2+accZ**2)))
    Rx = np.array([(1,0,0),(0,math.cos(Ax),-math.sin(Ax)),(0,math.sin(Ax),math.cos(Ax))])
    Ry = np.array([(math.cos(Ay),0,math.sin(Ay)),(0,1,0),(-math.sin(Ay),0,math.cos(Ay))])
    R = np.matmul(Rx, Ry)
    return R
    
class I2C_acc:
    
    def __init__(self,bus):
        self.i2c = bus
        self.i2c.try_lock()
        
        # Reset
        self.i2c.writeto(deviceAdd, bytes([control, 0x01]))             # go to standby
        self.i2c.writeto(deviceAdd, bytes([reset, 0x40]))               # power-on reset
        time.sleep(0.01)
        self.i2c.writeto(deviceAdd, bytes([feature, 0x40]))             # only enable I2C mode      
        self.i2c.writeto(deviceAdd, bytes([InitReg1, 0x42]))            
        self.i2c.writeto(deviceAdd, bytes([X_motion, 0x01]))
        self.i2c.writeto(deviceAdd, bytes([Y_motion, 0x80]))
        self.i2c.writeto(deviceAdd, bytes([Z_motion, 0x00]))
        self.i2c.writeto(deviceAdd, bytes([InitReg2, 0x00]))
        self.i2c.writeto(deviceAdd, bytes([InitReg3, 0x00]))            # finish

        self.i2c.writeto(deviceAdd, bytes([control, 0b001]))             # trig mod start from standby
        # settings
        self.i2c.writeto(deviceAdd, bytes([RangeAndReso, 0b010]))        #12 bits, +-2g
        self.i2c.writeto(deviceAdd, bytes([Trig_count,255]))
        self.xOffset = -0.1678
        self.yOffset = 0.005
        self.zOffset = 0.305

    def calibrate(self):
        print('initializing')
        for i in range(10):
            self.raw_data()
            time.sleep(0.1)
        print('place the sensor on surface and start calibration')
        cal_data = []
        for i in range(20):
            cal_data.append(self.raw_data())
            time.sleep(0.05)
        cal_mean = np.mean(cal_data,axis=0)
        self.xOffset = -cal_mean[0]
        self.yOffset = -cal_mean[1]
        self.zOffset = 9.807-cal_mean[2]
        
    def raw_data(self):
        self.i2c.writeto(deviceAdd, bytes([control, 0b10000111]))
        # self.reg_status()
        self.Wbuffer = bytes([X_DATA0])
        self.Rbuffer = bytearray(6)
        self.i2c.writeto_then_readfrom(deviceAdd, self.Wbuffer, self.Rbuffer)
        self.accX = unsign2signG(self.Rbuffer[1]<< 8 | self.Rbuffer[0]) + self.xOffset
        self.accY = unsign2signG(self.Rbuffer[3]<< 8 | self.Rbuffer[2]) + self.yOffset
        self.accZ = unsign2signG(self.Rbuffer[5]<< 8 | self.Rbuffer[4]) + self.zOffset
        
        # print([self.accX,self.accY,self.accZ] 
        return [self.accX, self.accY, self.accZ]
        
    def readnwrite_reg(self):
        self.i2c.writeto(deviceAdd, bytes([control, 0b10000111]))
        self.Rbuffer = bytearray(1)
        self.Wbuffer = bytes([X_DATA0])                          #  the register to read from
        self.i2c.writeto_then_readfrom(deviceAdd, self.Wbuffer, self.Rbuffer)
        return self.Rbuffer

    def reg_status(self):
        read_list = [status2,status]
        readback = []
        for i in read_list:
            self.Rt = bytearray(1)
            self.Wt = bytes([i]) 
            self.i2c.writeto_then_readfrom(deviceAdd, self.Wt, self.Rt)
            readback.append(self.Rt)
        # print(readback)
    
    def rot_matrix(self):
        self.R = rotMatrix(round(self.accX,4),round(self.accY,4),round(self.accZ,4))
        return self.R

    
# i2c = board.I2C()
# acc = I2C_acc(i2c)
# # acc.calibrate()
# print('start')
# acc_list = []

# for i in range (200):
#     acc_list.append(acc.raw_data())
#     time.sleep(0.05)

# filename = input('enter the file name: ')    
# file = open(filename + '_acc.txt', 'w')
# np.savetxt(file, np.array(acc_list))
# file.close()