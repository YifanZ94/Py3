"""
I2C mag collection
"""
import os 
os.environ["BLINKA_FT232H"] = "1"
import board
import busio
import struct

# from adafruit_register.i2c_struct import UnaryStruct, ROUnaryStruct

X_DATA_H = 0x69
X_DATA_L = 0x68
Y_DATA_H = 0x6B
Y_DATA_L = 0x6A
Z_DATA_H = 0x6D
Z_DATA_L = 0x6C

address = 0x1e
who_am_I = 0x4F

class I2C_mag():
    
    def __init__(self):
        self.i2c = busio.I2C(board.SCL, board.SDA)
        
    def get_data(self,add1,add2):
        self.i2c.try_lock()
        self.i2c.writeto(address, bytes([add1,add2]), stop=False)
        self.result = bytearray(2)
        self.i2c.readfrom_into(address,self.result)
        
        # self.r = self.result[0] << 8 | self.result[1]
        
        # self.r = struct.unpack('<h', self.result)

        # self.Gauss = (self.r *15)/10000
        self.i2c.unlock()
        
        return self.r

    def X_data(self):
        self.x_reading = self.get_data(X_DATA_H, X_DATA_L)
        return self.x_reading
    
    def Y_data(self):
        self.y_reading = self.get_data(Y_DATA_H,Y_DATA_L)
        return self.y_reading

    def Z_data(self):
        self.z_reading = self.get_data(Z_DATA_H,Z_DATA_L)
        return self.z_reading
    
    def all_data(self):
        self.mag_field = (self.X_data(),self.Y_data(),self.Z_data())
        return self.mag_field