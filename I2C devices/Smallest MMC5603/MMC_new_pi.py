import board
import time 
import busio

i2c = board.I2C()

deviceAdd = 0x30
identi_addr = 0x39
inter_control = 0x1b
X_H_add = 0x00

class Mag:
    def __init__(self):
        self.i2c = i2c
        self.i2c.writeto(deviceAdd, bytes([inter_control,0b00100001]))

    def all_data(self):
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

mag = Mag()
ans = mag.all_data()
print(ans)