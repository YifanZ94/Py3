import Adafruit_GPIO.FT232H as FT232H
import time
 
# Temporarily disable FTDI serial drivers.
FT232H.use_FT232H()
 
# Find the first FT232H device.
ft232h = FT232H.FT232H()
 
# Create an I2C device at address 0x70.
i2c = FT232H.I2CDevice(ft232h, 0x30)

X_Axis_Register_DATAX0 = 0x00
X_Axis_Register_DATAX1 = 0x01
Inter_control_0 = 0x1b

while True:
    
    i2c.write8(Inter_control_0, 1)

    X0 = i2c.readU8(X_Axis_Register_DATAX0)
    X1 = i2c.readU8(X_Axis_Register_DATAX1)
    r = (X0 << 8) + X1
    Gauss = (r/(65536.0) - 0.5)*60.0
    print("x1 =",X0, "x2 = ", X1)
    print('The measurement is', Gauss)
    time.sleep(0.2)
