# -*- coding: utf-8 -*-
"""
'MXC4005XC'

Read data via polling, I2C

-----------

**Hardware:**

* MEMSIC MXC4005XC accelerometer
  http://www.memsic.com/en/product/info.aspx?itemid=208&lcid=30#item208

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://circuitpython.org/downloads
* Adafruit's Bus Device library:
  https://github.com/adafruit/Adafruit_CircuitPython_BusDevice
* Adafruit's Register library:
  https://github.com/adafruit/Adafruit_CircuitPython_Register

"""
# import os 
# os.environ["BLINKA_FT232H"] = "1"         # different microcontroller


from micropython import const
from adafruit_register.i2c_struct import Struct, ROUnaryStruct
from adafruit_register.i2c_bits import RWBits
import adafruit_bus_device.i2c_device as i2cdevice

_MXC4005XC_ADDR = const(0x15)

_MXC4005XC_INT_0 = const(0x00)   
_MXC4005XC_INT_1 = const(0x01)
_MXC4005XC_STATUS = const(0x02)
_MXC4005XC_XOUT_MSB = const(0x03)   # XOUT[11:4] in D7-D0
_MXC4005XC_XOUT_LSB = const(0x04)   # XOUT[3:0] in D7-D4
_MXC4005XC_YOUT_MSB = const(0x05)   # YOUT[11:4] in D7-D0
_MXC4005XC_YOUT_LSB = const(0x06)   # YOUT[3:0] in D7-D4
_MXC4005XC_ZOUT_MSB = const(0x07)   # ZOUT[11:4] in D7-D0
_MXC4005XC_ZOUT_LSB = const(0x08)   # ZOUT[3:0] in D7-D4
_MXC4005XC_TOUT = const(0x09)       # TOUT[7:0]
_MXC4005XC_INT_MASK0 = const(0x0A)
_MXC4005XC_INT_MASK1 = const(0x0B)
_MXC4005XC_DETECTION = const(0x0C)
_MXC4005XC_CONTROL = const(0x0D)
_MXC4005XC_Who_Am_I = const(0x0F)

_STANDARD_GRAVITY = 9.80665


import math
import numpy as np

def XY_angle(accX,accY,accZ):
    Ax = math.atan(-accY/accZ)
    Ay = -math.atan(-accX/(math.sqrt(accY**2+accZ**2)))
    return [Ax,Ay]

def rotMatrix(Ax,Ay):
    Rx = np.array([(1,0,0),(0,math.cos(Ax),-math.sin(Ax)),(0,math.sin(Ax),math.cos(Ax))])
    Ry = np.array([(math.cos(Ay),0,math.sin(Ay)),(0,1,0),(-math.sin(Ay),0,math.cos(Ay))])
    R = np.matmul(Rx, Ry)
    return R

class Range:
    """An enum-like class representing the different
    acceleration measurement ranges. The values can be referenced like
    :attr:`Range.RANGE_2_G`
    
    Possible values are
    - :attr:`Range.RANGE_2_G`
    - :attr:`Range.RANGE_4_G`
    - :attr:`Range.RANGE_8_G`
    
    """
    
    RANGE_2_G = 0b00
    RANGE_4_G = 0b01  
    RANGE_8_G = 0b10  
    

class MXC4005XC:
    """Driver for the MXC4005XC Accelerometer.
    
    :param ~busio.I2C i2c_bus: The I2C bus the acc is connected to.
    
    **Quickstart: Importing and using the device**
    
        Here is an example of using the :class:`MC3672` class.
        First you will need to import the libraries to use the sensor
        
        .. code-block:: python
            import board
            import mxc4005xc
            
        Once this is done you can define your `board.I2C` object and 
        define your sensor object
        
        .. code-block:: python
            i2c = board.I2C()  # uses board.SCL and board.SDA
            acc = mxc4005xc.MXC4005XC(i2c)
            
        Now you have access to the :attr:`acceleration` attribute
        
        .. code-block:: python
            acc_x, acc_y, acc_z = acc.acceleration
    
    """
    
    def __init__(self, i2c_bus):
        self.i2c_device = i2cdevice.I2CDevice(i2c_bus, _MXC4005XC_ADDR)

        # set +/-2g range
        self.range = Range.RANGE_2_G

    # general settings
    range = RWBits(2, _MXC4005XC_CONTROL, 5)

    # data measurements
    _temp_raw = ROUnaryStruct(_MXC4005XC_TOUT, "B")
    _xyz_raw = Struct(_MXC4005XC_XOUT_MSB, ">hhh")

    @property
    def temperature(self):
        """The temperature returned in deg C
        """
        
        # 2's complement, range is -40 to +85C, 0 is temp at 25C
        # sensitivity is approx 0.586C/LSB
        res = 8
        if self._temp_raw < 2**(res-1):
            temp = self._temp_raw 
        else:
            temp = ((~self._temp_raw) + 1) & 0b01111111
            temp = -temp

        temp = (temp * 0.586) + 25
                
        return temp
        
    @property        
    def acceleration(self):
        """The x, y, z acceleration values returned in a
        3-tuple and are in :math:`m / s ^ 2`"""
        
        current_range = self.range
        scale = 1.0
        if current_range == 0: # +/- 2g, sensitivity 1024 LSB/g
            scale = 1024.0
        if current_range == 1: # +/- 4g, sensitivity 512 LSB/g
            scale = 512.0
        if current_range == 2: # +/- 8g, sensitivity 256 LSB/g
            scale = 256.0
        
        self.x, self.y, self.z = [((i >> 4) / scale) * _STANDARD_GRAVITY for i in self._xyz_raw]
        
        return [self.x, self.y, self.z+2]
    
    @property
    def acceleration_raw(self):
        
        x, y, z = [(i >> 4) for i in self._xyz_raw]
        
        return(bin(x), bin(y), bin(z))
        
#%%  test
    
# import board
# import time
# import numpy as np
# i2c = board.I2C() 
# acc = MXC4005XC(i2c)
# acc_data = []

# print("ready")
# while True:
#     try:
#         # reading = acc.acceleration
#         # print(reading)
#         # print(np.linalg.norm(reading))
#         acc_data.append(acc.acceleration)
#         time.sleep(0.01)
#     except:
#         break
  
# import matplotlib.pyplot as plt
# x = np.arange(len(acc_data))
# magData = np.array(acc_data)
# plt.plot(x,magData)
# plt.show()

# filename = input('enter the file name ')
# file = open(filename + '_mag.txt', 'w')
# np.savetxt(file, np.array(acc_data))
# file.close()