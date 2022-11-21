# -*- coding: utf-8 -*-
"""
Created on Wed Jun 24 17:24:01 2020

@author: Stephanie
Based on Adafruit examples

# CircuitPython driver for Memsic MMC5603NJ

**Software and Dependencies:**

* Adafruit CircuitPython firmware:
  https://circuitpython.org/downloads
* Adafruit's Bus Device library:
  https://github.com/adafruit/Adafruit_CircuitPython_BusDevice
* Adafruit's Register library:
  https://github.com/adafruit/Adafruit_CircuitPython_Register
"""

from time import sleep
from micropython import const 
    #used to declare the expression is a constant so that the compile can optimize?
from adafruit_bus_device.i2c_device import I2CDevice
from adafruit_register.i2c_struct import UnaryStruct, ROUnaryStruct
from adafruit_register.i2c_bit import RWBit, ROBit
from adafruit_register.i2c_bits import RWBits, ROBits


_ADDRESS_MAG = const(0x30) #0b0110000

# Magnetometer registers
Xout0 = const(0x00)        # Xout[19:12]
Xout1 = const(0x01)        # Xout[11:4]
Yout0 = const(0x02)        # Yout[19:12]
Yout1 = const(0x03)        # Yout[11:4]
Zout0 = const(0x04)        # Zout[19:12]
Zout1 = const(0x05)        # Zout[11:4]
Xout2 = const(0x06)        # Xout[3:0]
Yout2 = const(0x07)        # Yout[3:0]
Zout2 = const(0x08)        # Zout[3:0]
Tout = const(0x09)         # Temperature output
Status1 = const(0x18)      # Device status1
ODR = const(0x1A)          # Output data rate
Internal_control_0 = const(0x1B) # Control register 0
Internal_control_1 = const(0x1C) # Control register 1
Internal_control_2 = const(0x1D) # Control register 2
ST_X_TH = const(0x1E)      # X-axis selftest threshold
ST_Y_TH = const(0x1F)      # Y-axis selftest threshold
ST_Z_TH = const(0x20)      # Z-axis selftest threshold
ST_X = const(0x27)         # X-axis selftest set value
ST_Y = const(0x28)         # Y-axis selftest set value
ST_Z = const(0x29)         # Z-axis selftest set value
Product_ID = const(0x39)   # Product ID

class MMC5603NJ: 
    """
    Driver for the MMC5603NJ magnetometer
    
    :param busio.I2C i2c_bus: The I2C bus the mag is connected to
    """

    _BUFFER = bytearray(6)

    # _device_id = ROUnaryStruct(Product_ID, "B") # B = unsigned char/integer
    _device_id = ROBits(8, Product_ID, 0)
    # 0b 0001 0000

    # _raw_x0 = ROUnaryStruct(Xout0, "<h") # < = little-endian, h = short/integer
    # _raw_y0 = ROUnaryStruct(Yout0, "<h")
    # _raw_z0 = ROUnaryStruct(Zout0, "<h")
    _raw_x0 = ROBits(8, Xout0, 0)
    _raw_x1 = ROBits(8, Xout1, 0)
    _raw_x2 = ROBits(4, Xout2, 4)
    _raw_y0 = ROBits(8, Yout0, 0)
    _raw_y1 = ROBits(8, Yout1, 0)
    _raw_y2 = ROBits(4, Yout2, 4)
    _raw_z0 = ROBits(8, Zout0, 0)
    _raw_z1 = ROBits(8, Zout1, 0)
    _raw_z2 = ROBits(4, Zout2, 4)
    
    _raw_t = ROBits(8, Tout, 0)
    
    _status = ROUnaryStruct(Status1, "B")
    _sat_sensor = ROBit(Status1, 5)
    _meas_m_done = ROBit(Status1, 6)
    _meas_t_done = ROBit(Status1, 7)
    
    _odr = UnaryStruct(ODR, "B")
    
    _contr_reg_0 = RWBits(8, Internal_control_0, 0)
    _do_reset = RWBit(Internal_control_0, 4)
    _auto_sr_en = RWBit(Internal_control_0, 5)
    _cmm_freq_en = RWBit(Internal_control_0, 7)
    
    _bw = RWBits(2, Internal_control_1, 0)
    
    _cmm_en = RWBit(Internal_control_2, 4)    
    

    def __init__(self, i2c):
        self.i2c_device = I2CDevice(i2c, _ADDRESS_MAG)

        if self._device_id != 0x10:
            raise AttributeError("Cannot find an MMC5603NJ")
            
    def reset(self):
        """Do RESET to 'condition the AMR sensors for optimum performance  
        """
        self._do_reset = 1
        sleep(3)

    @property
    def magnetic_cmm(self):
        """The processed magnetometer sensor values.
        Print out measurements periodically
        
        :param float delay: sleep delay in seconds
        """
        
        delay = 3.0
        
        self.reset()
        
        # set bw?
        self._bw = 0b00
        
        # set automatic set/reset
        self._auto_sr_en = 1
        
        # write the desired number into output data rate
        self._odr = 1 # is this 75 Hz? with auto set/reset
        
        # set cmm_freq_en to 1 to calculate target number for the counter
        self._cmm_freq_en = 1
        
        # set cmm_en to 1 to start continous mode, internal counter starts
        self._cmm_en = 1
        
        sleep(1)
        
        # need to add a way to stop continuous measurements
        # press a button?
        while True:
            magx, magy, magz = self.magnetic_get_processed_mag_data()
            print("X:{0:7.2f}, Y:{1:7.2f}, Z:{2:7.2f} ".format(magx, magy, magz))
            sleep(delay)
            
        return()

    @property
    def magnetic_single(self):
        """The processed magnetometer sensor values.
        A tuple of X, Y, Z axis values.
        """
        # TM_M and Auto_SR_en high
        self._contr_reg_0 = 0b00100001
        
        # check Meas_M_Done bit
        while self._meas_m_done != 1:
            pass
               
        return self.magnetic_get_processed_mag_data()
    
    def magnetic_get_processed_mag_data(self):
        """
        Returns
        -------
        TYPE
            DESCRIPTION.
        TYPE
            DESCRIPTION.
        TYPE
            DESCRIPTION.
        """
        # Need to check math on this
        # 20 bit
        xval = (self._raw_x0<<12) | (self._raw_x1<<4) | (self._raw_x2)
        yval = (self._raw_y0<<12) | (self._raw_y1<<4) | (self._raw_y2)
        zval = (self._raw_z0<<12) | (self._raw_z1<<4) | (self._raw_z2)
        mask = 524288 
        xval = -(xval & mask) + (xval & ~mask)
        yval = -(yval & mask) + (yval & ~mask)
        zval = -(zval & mask) + (zval & ~mask)
        
        return (
            xval*0.0000625, yval*0.0000625, zval*0.0000625
        )

    @property
    def magnetic_raw(self):
        """The raw magnetometer sensor values.
        """
        # TM_M and Auto_SR_en high
        self._contr_reg_0 = 0b00100001
        
        # check Meas_M_Done bit
        while self._meas_m_done != 1:
            pass
        
        return self.magnetic_get_raw_mag_data()
    
    def magnetic_get_raw_mag_data(self):
        """
        Returns
        -------
        TYPE
            DESCRIPTION.
        TYPE
            DESCRIPTION.
        TYPE
            DESCRIPTION.
        TYPE
            DESCRIPTION.
        TYPE
            DESCRIPTION.
        TYPE
            DESCRIPTION.
        TYPE
            DESCRIPTION.
        TYPE
            DESCRIPTION.
        TYPE
            DESCRIPTION.

        """
        return (
            self._raw_x0, self._raw_x1, self._raw_x2,
            self._raw_y0, self._raw_y1, self._raw_y2,
            self._raw_z0, self._raw_z1, self._raw_z2,
        )

    @property
    def temperature(self):
        """The processed temperature output value in deg C. 
        (Unsigned format, range is -75 to 125 deg C, 00000000 stands for -75 deg C)
        """
        self._contr_reg_0 = 0b00100010
        
        while self._meas_t_done != 1:
            pass
        
        return (self._raw_t * (200/255)) - 75