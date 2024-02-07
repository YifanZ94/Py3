
import serial
import time

# Configure the serial port
ser = serial.Serial('/dev/ttyUSB0', 9600)  # Replace '/dev/ttyUSB0' with the appropriate port
ser.timeout = 1

# Read sensor data (replace with your own sensor reading code)
def read_sensor_data():
    # Read sensor data here and return it
    sensor_data = "Sensor Data"  # Replace with your actual sensor data
    return sensor_data

while True:
    # Read sensor data
    data = read_sensor_data()

    # Transmit the sensor data over Xbee
    ser.write(data.encode())

    # Delay between transmissions (if needed)
    time.sleep(1)
