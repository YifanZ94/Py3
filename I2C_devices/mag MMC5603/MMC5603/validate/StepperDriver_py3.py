# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 15:30:32 2019

@author: Stephanie

Modified from Pololu HighPowerStepperDriver code for Arduino

Need to add: 
    readReg()
    readStatus()
    readFaults()
    clearFaults()
    verifySettings()
    getDirection()
    
    
"""
import os 
os.environ["BLINKA_FT232H"] = "1"

import time
import board
import busio
import digitalio

from enum import Enum
import time


### Addresses of control and status registers.
class HPSDRegAddr(Enum):
    CTRL = 0x00
    TORQUE = 0x01
    OFF = 0x02
    BLANK = 0x03
    DECAY = 0x04
    STALL = 0x05
    DRIVE = 0x06
    STATUS = 0x07

### Possible arguments to setStepMode().
class HPSDStepMode(Enum):
    MicroStep256 = 0b1000
    MicroStep128 = 0b0111
    MicroStep64 = 0b0110
    MicroStep32 = 0b0101
    MicroStep16 = 0b0100
    MicroStep8 = 0b0011
    MicroStep4 = 0b0010
    MicroStep2 = 0b0001
    MicroStep1 = 0b0000

### Possible arguments to setDecayMode().
class HPSDDecayMode(Enum):
    Slow = 0b000
    SlowIncMixedDec = 0b001
    Fast = 0b010
    Mixed = 0b011
    SlowIncAutoMixedDec = 0b100
    AutoMixed = 0b101
    
### Bits that are set in the return value of readStatus() to indicate status
### conditions.
### See the DRV8711 datasheet for detailed descriptions of these status
### conditions.
#class HPSDStatusBit(Enum):
#    ### Overtemperature shutdown
#    OTS = 0
#    ### Channel A overcurrent shutdown
#    AOCP = 1
#    ### Channel B overcurrent shutdown
#    BOCP = 2
#    ### Channel A predriver fault
#    APDF = 3
#    ### Channel B predriver fault
#    BPDF = 4
#    ### Undervoltage lockout
#    UVLO = 5
#    ### Stall detected
#    STD = 6
#    ### Latched stall detect
#    STDLAT = 7

### Constructor
class HighPowerStepperDriver:

    def __init__(self):
        ### All settings set to power-on defaults
        self.ctrl = 0xC10
        self.torque = 0x1FF
        self.off = 0x030
        self.blank = 0x080
        self.decay = 0x110
        self.stall = 0x040
        self.drive = 0xA59
        
    def setupSPI(self):
        # Temporarily disable FTDI serial drivers.
        
         cs = digitalio.DigitalInOut(board.C0)
         cs.direction = digitalio.Direction.OUTPUT
         cs.value = True
         
         self.spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
    
    
#    def checkForDriver(self):
#        ft232devices = FT232H.enumerate_device_serials()
#        if len(ft232devices) >= 1:
#            return True
#        else:
#            return False
        
### Writes the specified value to a register
    ## Read/write bit and register address are the first 4 bits of the first
    ## byte; data is in the remaining 4 bits of the first byte combined with
    ## the second byte (12 bits total).
    ## The CS line must go low after writing for the value to actually take
    ## effect.
    def writeReg(self, address, data):
        self.spi.try_lock()
        
        all = ((address & 0b111) << 12) | (data & 0xFFF)
        message = [((all & (0b11111111 << 8)) >> 8), (all & 0b11111111)]
        self.spi.write(bytes([message[0], message[1]]))
        
        self.spi.unlock()
        
### Change all of the driver's settings back to their default values.
    ### It is good to call this near the beginning of your program to ensure that
    ### there are no settings left over from an earlier time that might affect the
    ### operation of the driver.
    def resetSettings(self):
        self.ctrl = 0xC10
        self.torque = 0x1FF
        self.off = 0x030
        self.blank = 0x080
        self.decay = 0x110
        self.stall = 0x040
        self.drive = 0xA59
        self.applySettings()
        
### Re-writes the cached settings stored in this class to the device.
    ### You should not normally need to call this function because settings are
    ### written to the device whenever they are changed.  However, if
    ### verifySettings() returns false (due to a power interruption, for
    ### instance), then you could use applySettings() to get the device's settings
    ### back into the desired state.
    def applySettings(self):
        self.writeTORQUE()
        self.writeOFF()      
        self.writeBLANK()
        self.writeDECAY()
        self.writeSTALL()
        self.writeDRIVE()
        
        ## CTRL is written last because it contains the ENBL bit, and we want to try
        ## to have all the other settings correct first.  (For example, TORQUE
        ## defaults to 0xFF (the maximum value), so it would be better to set a more
        ## appropriate value if necessary before enabling the motor.)
        self.writeCTRL()

    ### Writes the cached value of the CTRL register to the device.
    def writeCTRL(self):
        self.writeReg(HPSDRegAddr.CTRL.value, self.ctrl)

    ### Writes the cached value of the TORQUE register to the device.
    def writeTORQUE(self):
        self.writeReg(HPSDRegAddr.TORQUE.value, self.torque)

    ### Writes the cached value of the OFF register to the device.
    def writeOFF(self):
        self.writeReg(HPSDRegAddr.OFF.value, self.off)
        
    ### Writes the cached value of the BLANK register to the device.
    def writeBLANK(self):
        self.writeReg(HPSDRegAddr.BLANK.value, self.blank)

    ### Writes the cached value of the DECAY register to the device.
    def writeDECAY(self):
        self.writeReg(HPSDRegAddr.DECAY.value, self.decay)

    ### Writes the cached value of the STALL register to the device.
    def writeSTALL(self):
        self.writeReg(HPSDRegAddr.STALL.value, self.stall)

    ### Writes the cached value of the DRIVE register to the device.
    def writeDRIVE(self):
        self.writeReg(HPSDRegAddr.DRIVE.value, self.drive)
        
### Sets the driver's decay mode (DECMOD).
    ###
    ### Example usage:
    ### ~~~{.cpp}
    ### sd.setDecayMode(HPSDDecayMode::AutoMixed);
    ### ~~~
    def setDecayMode(self, decayMode):
        decay_mode = HPSDDecayMode[decayMode]
        # 7-0 are for TDECAY, 11 is reserved
        # so just need to set 10-8 in DECAY register
        self.decay = (self.decay & 0b00011111111) | ((decay_mode.value & 0b111) << 8)
        self.writeDECAY()


### Sets the current limit for a High-Power Stepper Motor Driver 36v4.
    ### The argument to this function should be the desired current limit in
    ### milliamps.
    ###
    ### WARNING: The 36v4 can supply up to about 4 A per coil continuously;
    ### higher currents might be sustainable for short periods, but can eventually
    ### cause the MOSFETs to overheat, which could damage them.  See the driver's
    ### product page for more information.
    ###
    ### This function allows you to set a current limit of up to 8 A (8000 mA),
    ### but we strongly recommend against using a current limit higher than 4 A
    ### (4000 mA) unless you are careful to monitor the MOSFETs' temperatures
    ### and/or restrict how long the driver uses the higher current limit.
    ### 
    ### This function takes care of setting appropriate values for ISGAIN and
    ### TORQUE to get the desired current limit.
    def setCurrentLimit(self, milliamps):
        if milliamps > 5000:
            milliamps = 5000
        
        isGainBits = 0b11
        torqueBits = int((768*milliamps)/6875)
        
        while torqueBits > 255:
            isGainBits = isGainBits - 1
            torqueBits = torqueBits >> 1
        
#         ISGAIN is 9-8 in CTRL register
#         TORQUE is 7-0 in TORQUE register
            
        self.ctrl = (self.ctrl & 0b110011111111) | (isGainBits << 8)
        self.writeCTRL()
        self.torque = (self.torque & 0b111100000000) | torqueBits
        self.writeTORQUE()

### Sets the driver's stepping mode (MODE).
    ### This affects many things about the performance of the motor, including how
    ### much the output moves for each step taken and how much current flows
    ### through the coils in each stepping position.
    ###
    ### Example usage:
    ### ~~~{.cpp}
    ### sd.setStepMode(HPSDStepMode::MicroStep32);
    ### ~~~
    def setStepMode(self, stepSize):
        step_size = HPSDStepMode[stepSize]
        # MODE is 6-3 in CTRL register
        self.ctrl = (self.ctrl & 0b111110000111) | (step_size.value << 3)
        self.writeCTRL()
        
### Clears any status conditions that are currently latched in the driver.
    ### WARNING: Calling this function clears latched faults, which might allow
    ### the motor driver outputs to reactivate.  If you do this repeatedly without
    ### fixing an abnormal condition (like a short circuit), you might damage the
    ### driver.
    def clearStatus(self):
        self.writeReg(HPSDRegAddr.STATUS.value, 0)
        
### Enables the driver (ENBL = 1).
    def enableDriver(self):
        self.ctrl |= (1 << 0)
        self.writeCTRL()
    
### Disables the driver (ENBL = 0).
    def disableDriver(self):
        self.ctrl &= ~(1 << 0)
        self.writeCTRL()

### Sets the motor direction (RDIR).
    ### Allowed values are 0 or 1.
    ### You can use this command to control the direction of the stepper motor and
    ### leave the DIR pin disconnected.
    def setDirection(self, dir):
        if (dir):
            self.ctrl |= (1 << 1)
        else:
            self.ctrl &= ~(1 << 1)
            
        self.writeCTRL()

### Advances the indexer by one step (RSTEP = 1).
    ### You can use this command to step the stepper motor and leave the STEP pin
    ### disconnected.
    ### The driver automatically clears the RSTEP bit after it is written.
    def step(self, steps, stepdelay):
        for i in range(steps):
            self.writeReg(HPSDRegAddr.CTRL.value, self.ctrl | (1 << 2))
            start_time = time.clock()
            while time.clock() - start_time < stepdelay:
                pass
    def step2(self, stepdelay):
        self.writeReg(HPSDRegAddr.CTRL.value, self.ctrl | (1 << 2))
        start_time = time.clock()
        while time.clock() - start_time < stepdelay:
            pass

## end HPSD class
