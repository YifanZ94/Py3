#***********************     Data Implementation      ***********************
""" The objective of this code is to to move robotic arm the foreram using the data
collected from the NORAXON IMUs. We collected data for the elbow flexion/extension and forearm roll at a rate of
200 Hz. Every 100th point of that data is being fed to two motors every second.
 """ 
# *******************************************************************************

import os
import time
import csv

if os.name == 'nt':
    import msvcrt
    def getch():
        return msvcrt.getch().decode()
else:
    import sys, tty, termios
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    def getch():
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

from dynamixel_sdk import * # Uses Dynamixel SDK library

# Importing position data from csv file
file = open("data2_090423.csv", "r")
data = list(csv.reader(file,delimiter = ","))
file.close()

# Turning flexion/extion data into a list
flex = [row[1] for row in data]
#Removing the string from list which is the heading
flex.pop(0)

#Turning foremarm roll data into a list
roll = [row[2]for row in data]
# Removing the string from the list, the heading.
roll.pop(0)

#********* DYNAMIXEL Model definition *********
MY_DXL = 'MX_SERIES'    # Motor series from Dynamixel Robotis 


# Control table address, according the eManual 
ADDR_TORQUE_ENABLE          = 64
ADDR_GOAL_POSITION          = 116
ADDR_PRESENT_POSITION       = 132
BAUDRATE                    = 57600

# Setting Drive mode for motor 1
ADDR_Drive_Mode             = 10
ADDR_Velocity_Profile       = 112

# DYNAMIXEL Protocol Version (2.0)
# https://emanual.robotis.com/docs/en/dxl/protocol2/
PROTOCOL_VERSION            = 2.0

# Setting IDs for the motor
DXL1_ID                      = 0 # Shoulder pitch
DXL2_ID                      = 1 # Shoulder roll
DXL3_ID                      = 2 # Shoulder yaw
DXL4_ID                      = 3 # Elbow flexion
DXL5_ID                      = 4 # Forearm roll 
DXL6_ID                      = 5 # Wrist pith  

# Setting the communication port
DEVICENAME                  = '/dev/ttyUSB0'

TORQUE_ENABLE               = 1     # Value for enabling the torque
TORQUE_DISABLE              = 0     # Value for disabling the torque
DXL_MOVING_STATUS_THRESHOLD = 20    # Dynamixel moving status threshold


#Setting ut time to achieve goal position
time_to_goal = 1000



# Setting index goal position for motor 1
#Converting the data from string sto integers.
dxl4_goal_position = [int(i) for i in flex]        # Goal position
dxl5_goal_position = [int(j) for j in roll] 

# Setting up reset position for each each motor (Robotic arm straight down)
dxl4_reset      = 2048
dxl5_reset      = 2048

# All motors will be reset at that withing the following time in milliseconds
motor_speed_reset = 5000

# Initialize PortHandler instance]
# Set the port path
# Get methods and members of PortHandlerLinux or PortHandlerWindows
portHandler = PortHandler(DEVICENAME)

# Initialize PacketHandler instance
# Set the protocol version
# Get methods and members of Protocol1PacketHandler or Protocol2PacketHandler
packetHandler = PacketHandler(PROTOCOL_VERSION)

# Open port
if portHandler.openPort():
    print("Succeeded to open the port")
else:
    print("Failed to open the port")
    print("Press any key to terminate...")
    getch()
    quit()


# Set port baudrate
if portHandler.setBaudRate(BAUDRATE):
    print("Succeeded to change the baudrate")
else:
    print("Failed to change the baudrate")
    print("Press any key to terminate...")
    getch()
    quit()

""" Enabliing the torque for all movement to prevent unwanted movement """

######  (Shoulder pitch) Motor 1 set up ##########
# Enable Dynamixel Torque
dxl1_comm_result, dxl1_error = packetHandler.write1ByteTxRx(portHandler, DXL1_ID, ADDR_TORQUE_ENABLE, TORQUE_ENABLE)
if dxl1_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(dxl1_comm_result))
elif dxl1_error != 0:
    print("%s" % packetHandler.getRxPacketError(dxl1_error))
else:
    print("Motor 1 has been successfully connected")

######################## (Shoulder roll) Motor 2 setup ###################################################################################

# Enable Motor Torque
dxl2_comm_result, dxl2_error = packetHandler.write1ByteTxRx(portHandler, DXL2_ID, ADDR_TORQUE_ENABLE, TORQUE_ENABLE)
if dxl2_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(dxl2_comm_result))
elif dxl1_error != 0:
    print("%s" % packetHandler.getRxPacketError(dxl2_error))
else:
    print("Motor 2 has been successfully connected")

######################## (Should yaw) Motor 3 setup ###################################################################################

# Enable Motor Torque
dxl3_comm_result, dxl3_error = packetHandler.write1ByteTxRx(portHandler, DXL3_ID, ADDR_TORQUE_ENABLE, TORQUE_ENABLE)
if dxl3_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(dxl3_comm_result))
elif dxl1_error != 0:
    print("%s" % packetHandler.getRxPacketError(dxl3_error))
else:
    print("Motor 3 has been successfully connected")

######################## (Elbow flexion/extention) Motor 4 setup ###################################################################################

# Enable Motor Torque
dxl4_comm_result, dxl4_error = packetHandler.write1ByteTxRx(portHandler, DXL4_ID, ADDR_TORQUE_ENABLE, TORQUE_ENABLE)
if dxl4_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(dxl4_comm_result))
elif dxl4_error != 0:
    print("%s" % packetHandler.getRxPacketError(dxl4_error))
else:
    print("Motor 4 has been successfully connected")

######################## (Forearm roll) Motor 5 setup ###################################################################################

# Enable Motor Torque
dxl5_comm_result, dxl5_error = packetHandler.write1ByteTxRx(portHandler, DXL5_ID, ADDR_TORQUE_ENABLE, TORQUE_ENABLE)
if dxl5_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(dxl5_comm_result))
elif dxl5_error != 0:
    print("%s" % packetHandler.getRxPacketError(dxl5_error))
else:
    print("Motor 5 has been successfully connected")

######################## (Wrist pitch) Motor 6 setup ###################################################################################

# Enable Motor  Torque
dxl6_comm_result, dxl6_error = packetHandler.write1ByteTxRx(portHandler, DXL6_ID, ADDR_TORQUE_ENABLE, TORQUE_ENABLE)
if dxl6_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(dxl6_comm_result))
elif dxl6_error != 0:
    print("%s" % packetHandler.getRxPacketError(dxl6_error))
else:
    print("Motor 6 has been successfully connected")


###############################################################################################################################
#Main operations:
while 1:
    print("Press any key to continue! (or press ESC to quit!)")
    if getch() == chr(0x1b):
        break

    # Write goal position and veloctity profile for each motor

    for i in range(0, len(flex),199):
        # Motor 1
            # Velocity profile set up
        dxl4_comm_result, dxl1_error = packetHandler.write4ByteTxRx(portHandler, DXL4_ID, ADDR_Velocity_Profile, time_to_goal)
            # Goal postition set up
        dxl4_comm_result, dxl1_error = packetHandler.write4ByteTxRx(portHandler, DXL4_ID, ADDR_GOAL_POSITION, dxl4_goal_position[i])

        # Motor 2
            # Velocity profile set up
        dxl5_comm_result, dxl5_error = packetHandler.write4ByteTxRx(portHandler, DXL5_ID, ADDR_Velocity_Profile, time_to_goal)
            # Goal postition set up
        dxl5_comm_result, dxl5_error = packetHandler.write4ByteTxRx(portHandler, DXL5_ID, ADDR_GOAL_POSITION, dxl5_goal_position[i])
            
            # Wait time for execution
        time.sleep(1)
        
        # Communication check for motor 4
        if dxl4_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl4_comm_result))
        elif dxl4_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl4_error))

        # Communication check for motor 5
        if dxl6_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl5_comm_result))
        elif dxl6_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl5_error))

        # Reset all motors after operation
        # Motor 4 (reset)
        dxl4_comm_result, dxl4_error = packetHandler.write4ByteTxRx(portHandler, DXL4_ID, ADDR_Velocity_Profile, motor_speed_reset)
        dxl4_comm_result, dxl4_error = packetHandler.write4ByteTxRx(portHandler, DXL4_ID, ADDR_GOAL_POSITION, dxl4_reset)
        if dxl4_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl4_comm_result))
        elif dxl4_error != 0:
            print("%s" % packetHandler.getTxRxResult(dxl4_error))

        # Motor 2 (reset)
        dxl5_comm_result, dxl5_error = packetHandler.write4ByteTxRx(portHandler, DXL5_ID, ADDR_Velocity_Profile, motor_speed_reset)
        dxl5_comm_result, dxl5_error = packetHandler.write4ByteTxRx(portHandler, DXL5_ID, ADDR_GOAL_POSITION, dxl5_reset)
        if dxl5_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl5_comm_result))
        elif dxl5_error != 0:
            print("%s" % packetHandler.getTxRxResult(dxl5_error))
    


# Disable Dynamixel Torque for motor 1
dxl1_comm_result, dxl1_error = packetHandler.write1ByteTxRx(portHandler, DXL1_ID, ADDR_TORQUE_ENABLE, TORQUE_DISABLE)
if dxl1_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(dxl1_comm_result))
elif dxl1_error != 0:
    print("%s" % packetHandler.getRxPacketError(dxl1_error))

# Disable Dynamixel Torque for motor 2
dxl2_comm_result, dxl2_error = packetHandler.write1ByteTxRx(portHandler, DXL2_ID, ADDR_TORQUE_ENABLE, TORQUE_DISABLE)
if dxl2_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(dxl2_comm_result))
elif dxl2_error != 0:
    print("%s" % packetHandler.getRxPacketError(dxl2_error))

# Disable Dynamixel Torque for motor 3
dxl3_comm_result, dxl3_error = packetHandler.write1ByteTxRx(portHandler, DXL3_ID, ADDR_TORQUE_ENABLE, TORQUE_DISABLE)
if dxl3_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(dxl3_comm_result))
elif dxl3_error != 0:
    print("%s" % packetHandler.getRxPacketError(dxl3_error))

# Disable Dynamixel Torque for motor 4
dxl4_comm_result, dxl4_error = packetHandler.write1ByteTxRx(portHandler, DXL4_ID, ADDR_TORQUE_ENABLE, TORQUE_DISABLE)
if dxl4_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(dxl4_comm_result))
elif dxl4_error != 0:
    print("%s" % packetHandler.getRxPacketError(dxl4_error))

# Disable Dynamixel Torque for motor 5
dxl5_comm_result, dxl5_error = packetHandler.write1ByteTxRx(portHandler, DXL5_ID, ADDR_TORQUE_ENABLE, TORQUE_DISABLE)
if dxl5_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(dxl5_comm_result))
elif dxl5_error != 0:
    print("%s" % packetHandler.getRxPacketError(dxl5_error))

# Disable Dynamixel Torque for motor 6
dxl6_comm_result, dxl2_error = packetHandler.write1ByteTxRx(portHandler, DXL6_ID, ADDR_TORQUE_ENABLE, TORQUE_DISABLE)
if dxl6_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(dxl6_comm_result))
elif dxl6_error != 0:
    print("%s" % packetHandler.getRxPacketError(dxl6_error))

# Close port
portHandler.closePort()
