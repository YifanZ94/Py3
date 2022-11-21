# This example is for use on (Linux) computers that are using CPython with
# Adafruit Blinka to support CircuitPython libraries. CircuitPython does
# not support PIL/pillow (python imaging library)!
#
# Ported to Pillow by Melissa LeBlanc-Williams for Adafruit Industries from Code available at:
# https://learn.adafruit.com/adafruit-oled-displays-for-raspberry-pi/programming-your-display

# Imports the necessary libraries...
import os 
os.environ["BLINKA_FT232H"] = "1"

import board
import digitalio
import PIL
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
import time
# Setting some variables for our reset pin etc.
RESET_PIN = digitalio.DigitalInOut(board.C0)

# Very important... This lets py-gaugette 'know' what pins to use in order to reset the display
i2c = board.I2C()
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3D, reset=RESET_PIN)

# Load a font in 2 different sizes.
font = ImageFont.truetype("F:\py code\I2C devices\OLED 1306\OpenSans-Bold.ttf", size= 20)
font2 = ImageFont.truetype("F:\py code\I2C devices\OLED 1306\OpenSans-Bold.ttf", size= 40)

# Draw the text

for i in range(10):
    # create display
    oled.fill(0)
    oled.show()
    # create blank image for drawing
    image = Image.new("1", (oled.width, oled.height))
    draw = ImageDraw.Draw(image)
    # draw
    draw.text((0, 0), "Location",font = font, fill=255)
    draw.text((20,30), "{}".format(i), font = font ,fill=255)
    # display
    oled.image(image)
    oled.show()
    
    time.sleep(1)



   