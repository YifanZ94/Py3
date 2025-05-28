"""
I2C mag collection
"""
import os 
os.environ["BLINKA_FT232H"] = "1"
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
address = 0x30

class I2C_mag():
    
    def __init__(self):
        self.Inter_control_0 = 0x1b
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.i2c.try_lock()
        
    def get_data(self,add1,add2):
        self.i2c.writeto(address, bytes([0x1b,1]), stop=True)
        self.i2c.writeto(address, bytes([add1,add2]), stop=True)
        result = bytearray(2)
        self.i2c.readfrom_into(address,result)
        self.r = result[0] << 8 | result[1]
        self.Gauss = (self.r/(65536.0) - 0.5)*60.0
        return self.Gauss    
    

    def X_data(self):
        self.x_reading = self.get_data(X_DATA0,X_DATA1)
        return self.x_reading
    
    def Y_data(self):
        self.y_reading = self.get_data(Y_DATA0,Y_DATA1)
        return self.y_reading

    def Z_data(self):
        self.z_reading = self.get_data(Z_DATA0,Z_DATA1)
        return self.z_reading
    
    def all_data(self):
        self.mag_field = (self.X_data(),self.Y_data(),self.Z_data())
        return self.mag_field
    
        
