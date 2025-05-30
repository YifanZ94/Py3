"""
I2C mag collection
"""
import os 
os.environ["BLINKA_FT232H"] = "1"
import board
import busio

X_DATAX0 = 0x00
X_DATAX1 = 0x01
Y_DATAX0 = 0x02
Y_DATAX1 = 0x03
Z_DATAX0 = 0x04
Z_DATAX1 = 0x05

address = 0x30

class I2C_mag:
    
    def __init__(self):
        self.Inter_control_0 = 0x1b
        self.i2c = busio.I2C(board.SCL, board.SDA)
        
    def get_data(self,add1,add2):
        self.i2c.try_lock()
        self.i2c.writeto(address, bytes([0x1b,1]), stop=False)
        self.i2c.writeto(address, bytes([add1,add2]), stop=False)
        result = bytearray(2)
        self.i2c.readfrom_into(address,result)
        self.i2c.unlock()
        self.r = result[0] << 8 | result[1]
        self.Gauss = (self.r/(65536.0) - 0.5)*60.0
        return self.Gauss    

    def X_data(self):
        self.x_reading = self.get_data(X_DATAX0,X_DATAX1)
        return self.x_reading
    
    def Y_data(self):
        self.y_reading = self.get_data(Y_DATAX0,Y_DATAX1)
        return self.y_reading

    def Z_data(self):
        self.z_reading = self.get_data(Z_DATAX0,Z_DATAX1)
        return self.z_reading
    
    def all_data(self):
        self.mag_field = (self.X_data(),self.Y_data(),self.Z_data())
        return self.mag_field