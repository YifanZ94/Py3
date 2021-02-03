# -*- coding: utf-8 -*-
"""
Created on Thu Jan  7 15:19:31 2021

@author: Administrator
"""

import os 
# os.environ["BLINKA_MCP2221"] = "1"
os.environ["BLINKA_FT232H"] = "1"         # different microcontroller
import board
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
    
class I2C_acc:
    
    def __init__(self):
        self.i2c = board.I2C()
        self.i2c.try_lock()
        
        # Reset
        self.i2c.writeto(deviceAdd, bytes([control, 0x01]))             # go to standby
        self.i2c.writeto(deviceAdd, bytes([reset, 0x40]))               # power-on reset
        time.sleep(0.01)
        self.i2c.writeto(deviceAdd, bytes([feature, 0x40]))             # only enable I2C mode      
        time.sleep(0.01)
        self.i2c.writeto(deviceAdd, bytes([InitReg1, 0x42]))            
        self.i2c.writeto(deviceAdd, bytes([X_motion, 0x01]))
        self.i2c.writeto(deviceAdd, bytes([Y_motion, 0x80]))
        self.i2c.writeto(deviceAdd, bytes([Z_motion, 0x00]))
        self.i2c.writeto(deviceAdd, bytes([InitReg2, 0x00]))
        self.i2c.writeto(deviceAdd, bytes([InitReg3, 0x00]))            # finish

        self.i2c.writeto(deviceAdd, bytes([control, 0b001]))             # trig mod start from standby
        # settings
        self.i2c.writeto(deviceAdd, bytes([RangeAndReso, 0b010]))        #12 bits, +-2g
        self.i2c.writeto(deviceAdd, bytes([Trig_count,0x01]))
        self.reg_status()
        
    def get_data(self):
        self.i2c.writeto(deviceAdd, bytes([control, 0b10000111]))
        self.reg_status()
        self.Wbuffer = bytes([X_DATA0])
        self.Rbuffer = bytearray(6)
        self.i2c.writeto_then_readfrom(deviceAdd, self.Wbuffer, self.Rbuffer)
        # self.Wbuffer2 = bytes([Z_DATA0])
        # self.Rbuffer2 = bytearray(2)
        # self.i2c.writeto_then_readfrom(deviceAdd, self.Wbuffer2, self.Rbuffer2)
        # self.reg_status()
        self.Xresult = self.Rbuffer[1]<< 8 | self.Rbuffer[0]
        self.Yresult = self.Rbuffer[3]<< 8 | self.Rbuffer[2]
        self.Zresult = self.Rbuffer[5]<< 8 | self.Rbuffer[4]
        # self.Zresult = self.Rbuffer2[1]<< 8 | self.Rbuffer2[0]
        
        self.i2c.unlock()
        return [unsign2signG(self.Xresult),unsign2signG(self.Yresult),unsign2signG(self.Zresult)+0.3]
        # return [self.Xresult,self.Yresult,self.Zresult]
    
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
        print(readback)
    
    
acc = I2C_acc()
# ans = acc.readnwrite_reg()
ans = acc.get_data()
print(ans)
# print(bin(ans[0]),bin(ans[1]),bin(ans[2]))
