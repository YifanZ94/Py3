
from time import sleep
from micropython import const
from adafruit_bus_device.i2c_device import I2CDevice
from adafruit_register.i2c_bit import RWBit
from adafruit_register.i2c_struct import UnaryStruct, ROUnaryStruct
from adafruit_register.i2c_bits import RWBits


#__version__ = "0.0.0-auto.0"
#__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_LIS2MDL.git"

# pylint: disable=bad-whitespace
_ADDRESS_MAG = const(0x30)  # (0x3C >> 1)       // 0011110x

#MAG_DEVICE_ID = 0b01000000

# Magnetometer registers
OUTX_L_REG = 0x00
OUTX_H_REG = 0x01
OUTY_L_REG = 0x02
OUTY_H_REG = 0x03
OUTZ_L_REG = 0x04
OUTZ_H_REG = 0x05

Inter_control = 0x1b
# pylint: enable=bad-whitespace


class MMC5603:  # pylint: disable=too-many-instance-attributes

    
    _enable = RWBit(Inter_control, 0, 1)

    _raw_x_0 = ROUnaryStruct(OUTX_L_REG, "<B")
    _raw_x_1 = ROUnaryStruct(OUTX_H_REG, "<B")
    
#    _raw_y = ROUnaryStruct(OUTY_L_REG, "<h")
#    _raw_z = ROUnaryStruct(OUTZ_L_REG, "<h")


    def __init__(self, i2c):
        self.i2c_device = I2CDevice(i2c, _ADDRESS_MAG)
#
#        if self._device_id != 0x40:
#            raise AttributeError("Cannot find an LIS2MDL")
#
        self.reset()
        
        
    def reset(self):
        """Reset the sensor to the default state set by the library"""
        self._soft_reset = True
        sleep(0.100)
        self._reboot = True
        sleep(0.100)
        self._mode = 0x00
        self._bdu = True  # Make sure high and low bytes are set together
        self._int_latched = True
        self._int_reg_polarity = True
        self._int_iron_off = False
        self._interrupt_pin_putput = True
        self._temp_comp = True

        sleep(0.030)  # sleep 20ms to allow measurements to stabilize

    @property
    def magnetic(self):
        """The processed magnetometer sensor values.
        A 3-tuple of X, Y, Z axis values in microteslas that are signed floats.
        """
        self._enable = 1
        
        return (
            self._raw_x_0,
            self._raw_x_1,
        )

