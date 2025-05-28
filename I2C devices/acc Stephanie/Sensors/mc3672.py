# -*- coding: utf-8 -*-
"""
'MC3672'

Read data via polling, I2C

-----------

**Hardware:**

* MEMSIC MC3672 accelerometer
  http://www.memsic.com/en/product/info.aspx?itemid=392&lcid=49#item392

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://circuitpython.org/downloads
* Adafruit's Bus Device library:
  https://github.com/adafruit/Adafruit_CircuitPython_BusDevice
* Adafruit's Register library:
  https://github.com/adafruit/Adafruit_CircuitPython_Register
  
"""

import time 

from micropython import const
from adafruit_register.i2c_struct import Struct
from adafruit_register.i2c_bit import RWBit
from adafruit_register.i2c_bits import RWBits
import adafruit_bus_device.i2c_device as i2cdevice

_MC3672_ADDR = const(0x4C)

_MC3672_EXT_STAT_1 = const(0x00)
_MC3672_EXT_STAT_2 = const(0x01)    
_MC3672_XOUT_LSB = const(0x02)
_MC3672_XOUT_MSB = const(0x03)
_MC3672_YOUT_LSB = const(0x04)
_MC3672_YOUT_MSB = const(0x05)
_MC3672_ZOUT_LSB = const(0x06)
_MC3672_ZOUT_MSB = const(0x07)
_MC3672_STATUS_1 = const(0x08)
_MC3672_STATUS_2 = const(0x09)

_MC3672_FREG_1 = const(0x0D)
_MC3672_FREG_2 = const(0x0E)
_MC3672_INIT_1 = const(0x0F)
_MC3672_MODE_C = const(0x10)
_MC3672_RATE_1 = const(0x11)
_MC3672_SNIFF_C = const(0x12)       # sniff control
_MC3672_SNIFFTH_C = const(0x13)     # sniff threshold control
_MC3672_SNIFFCF_C = const(0x14)     # sniff configuration
_MC3672_RANGE_C = const(0x15)       # range resolution control
_MC3672_FIFO_C = const(0x16)        # FIFO control
_MC3672_INTR_C = const(0x17)        # interrupt control

_MC3672_INIT_3 = const(0x1A)
_MC3672_SCRATCH = const(0x1B)       # scratchpad
_MC3672_PMCR = const(0x1C)          # power control mode

_MC3672_DMX = const(0x20)           # drive motion X
_MC3672_DMY = const(0x21)           # drive motion Y
_MC3672_DMZ = const(0x22)           # drive motion Z

_MC3672_RESET = const(0x24)

_MC3672_INIT_2 = const(0x28)
_MC3672_TRIGC = const(0x29)         # trigger count
_MC3672_XOFFL = const(0x2A)         # X-offset LSB
_MC3672_XOFFH = const(0x2B)         # X-offset MSB
_MC3672_YOFFL = const(0x2C)         # Y-offset LSB
_MC3672_YOFFH = const(0x2D)         # Y-offset MSB
_MC3672_ZOFFL = const(0x2E)         # Z-offset LSB
_MC3672_ZOFFH = const(0x2F)         # Z-offset MSB
_MC3672_XGAIN = const(0x30)
_MC3672_YGAIN = const(0x31)
_MC3672_ZGAIN = const(0x32)


_STANDARD_GRAVITY = 9.80665

class Mode: 
    """An enum-like class representing the different operating modes. 
    The values can be referenced like :attr:`Mode.SWAKE`
    
    Possible values are
    - :attr:`Mode.SLEEP`
    - :attr:`Mode.STANDBY`
    - :attr:`Mode.SNIFF`
    - :attr:`Mode.CWAKE`
    - :attr:`Mode.SWAKE`
    - :attr:`Mode.TRIG`
    
    """
    SLEEP = 0b000
    STANDBY = 0b001
    SNIFF = 0b010
    CWAKE = 0b101   
    SWAKE = 0b110
    TRIG = 0b111

class PowerMode:
    """An enum-like class representing the different power modes. 
    The values can be referenced like :attr:`PowerMode.LOW_POWER`
    
    Possible values are
    - :attr:`PowerMode.LOW_POWER`
    - :attr:`PowerMode.ULTRA_LOW_POWER`
    - :attr:`PowerMode.PRECISION`
    
    """

    LOW_POWER = 0b000       # default, nominal noise levels
    ULTRA_LOW_POWER = 0b011 # highest noise levels
    PRECISION = 0b100       # lowest noise levels

class DataRate:
    """An enum-like class representing the different data rates. 
    The data rate changes based on the power mode.
    Ultra Low Power: 25-1300 Hz
    Low Power: 14-750 Hz
    Precision: 14-100 Hz
    The values can be referenced like :attr:`DataRate.RATE_100_HZ`
    
    Possible values are
    - :attr:`DataRate.RATE_25_HZ`
    - :attr:`DataRate.RATE_50_HZ`
    - :attr:`DataRate.RATE_100_HZ`
    - :attr:`DataRate.RATE_190_HZ`
    - :attr:`DataRate.RATE_380_HZ`
    - :attr:`DataRate.RATE_750_HZ`
    - :attr:`DataRate.RATE_1100_HZ`
    
    """

    RATE_25_HZ = 0x06
    RATE_50_HZ = 0x07
    RATE_100_HZ = 0x08
    RATE_190_HZ = 0x09
    RATE_380_HZ = 0x0A
    RATE_750_HZ = 0x0B
    RATE_1100_HZ = 0x0C

class ClockRate:
    """An enum-like class representing the different standby 
    clock rates. The rate changes based on the power mode.
    The values can be referenced like :attr:`DataRate.RATE_180`
    
    Possible values are
    - :attr:`ClockRate.RATE_1`
    - :attr:`ClockRate.RATE_3`
    - :attr:`ClockRate.RATE_5`
    - :attr:`ClockRate.RATE_10`
    - :attr:`ClockRate.RATE_23`
    - :attr:`ClockRate.RATE_45`
    - :attr:`ClockRate.RATE_90`
    - :attr:`ClockRate.RATE_180`
    
    """
                        # ultra-low / low / precision
    RATE_1 = 0b000      # 1 / 0.5 / 0.1   default
    RATE_3 = 0b001      # 3 / 1 / 0.2
    RATE_5 = 0b010      # 5 / 3 / 0.4
    RATE_10 = 0b011     # 10 / 6 / 0.8
    RATE_23 = 0b100     # 23 / 12 / 1.5
    RATE_45 = 0b101     # 45 / 24 / 3
    RATE_90 = 0b110     # 90 / 48 / 5
    RATE_180 = 0b111    # 180 / 100 / 10

class Range:
    """An enum-like class representing the different
    acceleration measurement ranges. The values can be 
    referenced like :attr:`Range.RANGE_2_G`
    
    Possible values are
    - :attr:`Range.RANGE_2_G`
    - :attr:`Range.RANGE_4_G`
    - :attr:`Range.RANGE_8_G`
    - :attr:`Range.RANGE_12_G`
    - :attr:`Range.RANGE_16_G`
    
    """
    
    RANGE_2_G = 0b000  # +/- 2g (default value)
    RANGE_4_G = 0b001  # +/- 4g
    RANGE_8_G = 0b010  # +/- 8g
    RANGE_16_G = 0b011  # +/- 16g
    RANGE_12_G = 0b100  # +/- 12g
    
class Resolution:
    """An enum-like class representing the different
    measurement ranges. The values can be referenced like
    :attr:`Range.RESOLUTION_12_BIT`
    
    Possible values are
    - :attr:`Resolution.RESOLUTION_14_BIT`
    - :attr:`Resolution.RESOLUTION_12_BIT`
    - :attr:`Resolution.RESOLUTION_10_BIT`
    - :attr:`Resolution.RESOLUTION_8_BIT`
    - :attr:`Resolution.RESOLUTION_7_BIT`
    - :attr:`Resolution.RESOLUTION_6_BIT`
    
    """

    RESOLUTION_6_BIT = 0b000
    RESOLUTION_7_BIT = 0b001
    RESOLUTION_8_BIT = 0b010
    RESOLUTION_10_BIT = 0b011
    RESOLUTION_12_BIT = 0b100
    RESOLUTION_14_BIT = 0b101 # only 12-bits if FIFO enabled


class MC3672:
    """Driver for the MC3672 Accelerometer.
    
    :param ~busio.I2C i2c_bus: The I2C bus the acc is connected to.
    
    **Quickstart: Importing and using the device**
    
        Here is an example of using the :class:`MC3672` class.
        First you will need to import the libraries to use the sensor
        
        .. code-block:: python
            import board
            import mc3672
            
        Once this is done you can define your `board.I2C` object and 
        define your sensor object
        
        .. code-block:: python
            i2c = board.I2C()  # uses board.SCL and board.SDA
            acc = mc3672.MC3672(i2c)
            
        Now you have access to the :attr:`acceleration` attribute
        
        .. code-block:: python
            acc.set_trigger_continous()
            acc_x, acc_y, acc_z = acc.acceleration
    """
    
    def __init__(self, i2c_bus):
        self.i2c_device = i2cdevice.I2CDevice(i2c_bus, _MC3672_ADDR)

        # Recommended initialization sequence for I2C interface
        
        # Go to standby
        self.operation_mode = Mode.STANDBY
        
        # Reset (or Power-On)
        self._reset = 1     # force a power-on-reset (POR) sequence
        
        # Wait at least 1 msec
        time.sleep(0.01)
        
        # Enable I2C mode
        self._i2c_enable = 1 # disables any SPI communications
        
        # Initializations
        self._init_1 = 0x42
        self._init_dmx = 0x01
        self._init_dmy = 0x80
        self._init_dmz = 0x00
        self._init_2 = 0x00
        self._init_3 = 0x00
        
        # set +/-2g range, 14 bit resolution, 
        # precision power mode, and 80 Hz data rate
        # mag ODR from 75 to 255-1000 Hz
        self.range = Range.RANGE_2_G
        self.resolution = Resolution.RESOLUTION_14_BIT
        self.power_mode_cspm = PowerMode.PRECISION
        self.data_rate = DataRate.RATE_100_HZ   # = 80 Hz in Precision
        
        # trigger mode ignores setting in ODR, uses the STB_Rate[2:0]
        # clock setting as the sampling rate
        self.standby_clock_rate = ClockRate.RATE_180
        
        self.scale = self.calculate_scale()
        
    _reset = RWBit(_MC3672_RESET, 6)
    _i2c_enable = RWBit(_MC3672_FREG_1, 6)
    _init_1 = RWBits(8, _MC3672_INIT_1, 0)
    _init_dmx = RWBits(8, _MC3672_DMX, 0)
    _init_dmy = RWBits(8, _MC3672_DMY, 0)
    _init_dmz = RWBits(8, _MC3672_DMZ, 0)
    _init_2 = RWBits(8, _MC3672_INIT_2, 0)
    _init_3 = RWBits(8, _MC3672_INIT_3, 0)
    
    _scale = 4096
    
    # set to execute trigger mode, only from standby
    _trig_cmd = RWBit(_MC3672_MODE_C, 7)    
    
    # general settings
    operation_mode = RWBits(3, _MC3672_MODE_C, 0)
    range = RWBits(3, _MC3672_RANGE_C, 4)
    resolution = RWBits(3, _MC3672_RANGE_C, 0)
    data_rate = RWBits(4, _MC3672_RATE_1, 0)
    power_mode_cspm = RWBits(3, _MC3672_PMCR, 0)    # CWAKE, SWAKE Power Mode
    power_mode_spm = RWBits(3, _MC3672_PMCR, 4)     # SNIFF Power Mode
    trigger_count = RWBits(8, _MC3672_TRIGC, 0)
    standby_clock_rate = RWBits(3, _MC3672_SNIFF_C, 5)

    # data measurements
    _xyz_raw = Struct(_MC3672_XOUT_LSB, "<hhh")

    def calculate_scale(self):
        
        current_resolution = self.resolution
        res = 14
        if current_resolution == 0:
            res = 6
        if current_resolution == 1:
            res = 7
        if current_resolution == 2:
            res = 8
        if current_resolution == 3:
            res = 10
        if current_resolution == 4:
            res = 12
        if current_resolution == 5:
            res = 14
        
        current_range = self.range
        scale = 1.0
        if current_range == 0: # 2g
            scale = 2**(res-2)
        if current_range == 1: # 4g
            scale = 2**(res-3)
        if current_range == 2: # 8g
            scale = 2**(res-4)
        if current_range == 3: # 16g
            scale = 2**(res-5)
        if current_range == 4: # 12g
            scale = 2**(res-1)/12
        
        return scale

    def set_trigger_continous(self):
        # standby
        self.operation_mode = Mode.STANDBY
        time.sleep(0.01)
        
        # set trigger count to continuous
        self.trigger_count = 255
        
        # set to trigger mode
        self.operation_mode = Mode.TRIG
        
        # execute trigger mode
        self._trig_cmd = 1
        time.sleep(0.02)
        
    @property        
    def acceleration(self):
        """The x, y, z acceleration values returned in a
        3-tuple and are in :math:`m / s ^ 2`"""
        
        x, y, z = [((i) / self._scale) * _STANDARD_GRAVITY for i in self._xyz_raw]
        
        return (x, y, z)
    
    @property
    def acceleration_raw(self):
     
        x, y, z = [i for i in self._xyz_raw]
        return(bin(x), bin(y), bin(z))
        

    