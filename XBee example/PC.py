import serial

# Configure the serial port
ser = serial.Serial('COM1', 9600)  # Replace 'COM1' with the appropriate port
ser.timeout = 1

# Open a file to save the received sensor data
file_path = "sensor_data.txt"
file = open(file_path, "a")

while True:
    # Read the incoming data from Xbee
    data = ser.readline().decode().strip()

    # Save the sensor data to a file
    file.write(data + "\n")
    file.flush()  # Ensure data is written immediately

    # Print the received data (optional)
    print("Received data:", data)
