import time
import board
import busio
import adafruit_lsm9ds1
import struct

i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_lsm9ds1.LSM9DS1_I2C(i2c)
ACCELRANGE_2G = 0b00 << 3
ACCELRANGE_16G = 0b01 << 3
ACCELRANGE_4G = 0b10 << 3
ACCELRANGE_8G = 0b11 << 3
MAGGAIN_4GAUSS = 0b00 << 5  # +/- 4 gauss
MAGGAIN_8GAUSS = 0b01 << 5  # +/- 8 gauss
MAGGAIN_12GAUSS = 0b10 << 5  # +/- 12 gauss
MAGGAIN_16GAUSS = 0b11 << 5  # +/- 16 gauss
GYROSCALE_245DPS = 0b00 << 3  # +/- 245 degrees/s rotation
GYROSCALE_500DPS = 0b01 << 3  # +/- 500 degrees/s rotation
GYROSCALE_2000DPS = 0b11 << 3  # +/- 2000 degrees/s rotation
sensor.accel_range = ACCELRANGE_4G


from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService

ble = BLERadio()
uart = UARTService()
advertisement = ProvideServicesAdvertisement(uart)

while True:
    ble.start_advertising(advertisement)
    print("Waiting to connect")
    while not ble.connected:
        pass
    print("Connected")

    while ble.connected:
        s = uart.readline()
        if s:
            gyro_x, gyro_y, gyro_z = sensor.gyro
            acc_x, acc_y, acc_z = sensor.acceleration

            # data = [acc_x, acc_y, acc_z, gyro_x-0.015, gyro_y+0.065, gyro_]
            # result = str(data)
            # uart.write(result.encode("utf-8"))

            ba = bytearray(struct.pack("6fs", acc_x, acc_y, acc_z, gyro_x, gyro_y, gyro_z, b'\n'))
            uart.write(ba)

        else:
            pass
