"""
I2C mag collection
"""

import board
import busio

# for lisd magnetometer
# X_DATAX0 = 0x69
# X_DATAX1 = 0x68
# Y_DATAX0 = 0x6B
# Y_DATAX1 = 0x6A
# Z_DATAX0 = 0x6D
# Z_DATAX1 = 0x6C
# address = 0x1e

# for MMC magnetometer

X_DATA0 = 0x00
X_DATA1 = 0x01
Y_DATA0 = 0x02
Y_DATA1 = 0x03
Z_DATA0 = 0x04
Z_DATA1 = 0x05
status_add = 0x18
address = 0x30
Inter_control_0 = 0x1b

class I2C_mag():
    
    def __init__(self):
        self.i2c = busio.I2C(board.SCL, board.SDA)
        # self.i2c.try_lock()
        
    def get_data(self, addr):
        self.i2c.writeto(address, bytes([0x1b,1]), stop=False)
        
        self.i2c.writeto(address, bytes([status_add]), stop=False)
        status = bytearray(1)
        self.i2c.readfrom_into(address,status)
        
        if not status[0] & (1 << (7-1)):             
            self.i2c.writeto(address, bytes([addr]), stop=True)
            result = bytearray(2)
            self.i2c.readfrom_into(address,result)
            self.r = result[0] << 8 | result[1]
            self.Gauss = (self.r/(65536.0) - 0.5)*60.0
            return self.Gauss    
        
        else:
            print("NOT READY") 
            
    def all_data(self):
        self.group = [self.get_data(X_DATA0),self.get_data(Y_DATA0),self.get_data(Z_DATA0)]
        return self.group

# subject = I2C_mag()
# subject.all_data()  
        
