# -*- coding: utf-8 -*-
"""
Created on Thu Jan  7 15:19:31 2021

@author: Administrator
"""

import os 
os.environ["BLINKA_MCP2221"] = "1"
# os.environ["BLINKA_FT232H"] = "1"         # different microcontroller
import board
import busio
import time 

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

buffer = bytes([X_DATA0,X_DATA1,Y_DATA0,Y_DATA1,Z_DATA0,Z_DATA1])

# change from 2's complement
def unsign2signG(unsign):
    unsign_str = str(bin(unsign))[2:]
    ordi = len(unsign_str)
    
    # unsign = int(unsign_str,2)
    if unsign < 2**(ordi-1):
        # signed = -(2**order - int(raw[6:],2))
        # print('+')
        signed = unsign
    else:
        # print('-')
        signed = -(2**ordi - unsign)
                   
    return (signed/128)*19.614
    
class I2C_acc:
    
    def __init__(self):
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.i2c.try_lock()
        
        # initialize
        self.i2c.writeto(deviceAdd, bytes([control, 0x01]))             # go to standby
        self.i2c.writeto(deviceAdd, bytes([reset, 0x40]))               # power-on reset
        time.sleep(0.1)
        self.i2c.writeto(deviceAdd, bytes([feature, 0x40]))             # only enable I2C mode        
        self.i2c.writeto(deviceAdd, bytes([InitReg1, 0x42]))            
        self.i2c.writeto(deviceAdd, bytes([X_motion, 0x01]))
        self.i2c.writeto(deviceAdd, bytes([Y_motion, 0x80]))
        self.i2c.writeto(deviceAdd, bytes([Z_motion, 0x00]))
        self.i2c.writeto(deviceAdd, bytes([InitReg2, 0x00]))
        self.i2c.writeto(deviceAdd, bytes([InitReg3, 0x00]))            #  finish initialization
        
        # to be modified 
        self.i2c.writeto(deviceAdd, bytes([control, 0b001]))             # trig mod start from standby
        # settings
        self.i2c.writeto(deviceAdd, bytes([Trig_count, 0x01]))          # set sample number
        self.i2c.writeto(deviceAdd, bytes([RangeAndReso, 0b010]))        #12 bits, +-2g

        # self.i2c.writeto(deviceAdd, bytes([scratch_pad, 0x06]))       # send trig commd
        
    def get_data(self):
        self.i2c.writeto(deviceAdd, bytes([control, 0b10000111]))

        self.Wbuffer = buffer
        self.Rbuffer = bytearray(6)
        self.i2c.writeto_then_readfrom(deviceAdd, self.Wbuffer, self.Rbuffer)
        # self.i2c.writeto(deviceAdd, bytes([add1,add2]))
        # result = bytearray(2)
        # self.i2c.readfrom_into(deviceAdd,result)
        self.Xresult = self.Rbuffer[4]<< 8 | self.Rbuffer[5]
        self.Yresult = self.Rbuffer[2]<< 8 | self.Rbuffer[3]
        self.Zresult = self.Rbuffer[0]<< 8 | self.Rbuffer[1]
        
        self.i2c.unlock()
        return [unsign2signG(self.Xresult),unsign2signG(self.Yresult),unsign2signG(self.Zresult)]
        # return [self.Xresult,self.Yresult,self.Zresult]
    
    def read_reg(self):
        self.Rbuffer = bytearray(1)
        self.Wbuffer = bytes([Trig_count])                          #  the register to read from
        self.i2c.writeto_then_readfrom(deviceAdd, self.Wbuffer, self.Rbuffer)
        return self.Rbuffer
        
    
acc = I2C_acc()
# ans = acc.read_reg()
ans = acc.get_data()
print(ans)
# print(bin(ans[0]),bin(ans[1]),bin(ans[2]))