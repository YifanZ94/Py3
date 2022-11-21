import numpy as np
import cv2 as cv

#find HSV of tennis ball
#Here you can change the values based off of the RGB color of your object. 
#Keep in mind this is taking in the values by BGR, so make sure you adjust the values accordingly.
green = np.uint8([[[167, 61, 249]]])

hsv_green = cv.cvtColor(green, cv.COLOR_BGR2HSV)

print(hsv_green)

#based off of the outputted value, you should take the value for H and add +- 10. This will create your upper and lower bound for H. 
#For S and V, assign lower to be 100 for both and assign V to be 255 for both. You can adjust these values accoridngly, but mainly play
#arround with the H value to adjust what color you are identifying. 
