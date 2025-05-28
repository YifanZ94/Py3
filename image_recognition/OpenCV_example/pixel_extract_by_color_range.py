# -*- coding: utf-8 -*-
"""
Created on Wed Mar 12 11:46:32 2025

@author: a4945
"""

import cv2
import numpy as np

# Initialize global variables
ref_color = None
tolerance = 40  # Adjust this value for color similarity sensitivity

#%%
def select_pixel(event, x, y, flags, param):
    global ref_color
    if event == cv2.EVENT_LBUTTONDOWN:
        # Get the BGR color of the clicked pixel
        ref_color = image[y, x]
        print(f"Selected color (BGR): {ref_color}")

        # Define the color range based on the selected pixel and tolerance
        lower_bound = np.maximum(ref_color - tolerance, 0)
        upper_bound = np.minimum(ref_color + tolerance, 255)

        # Create a mask that identifies all pixels within the color range
        mask = cv2.inRange(image, lower_bound, upper_bound)

        # Extract the pixels that match the color criteria
        result = cv2.bitwise_and(image, image, mask=mask)

        # Display the result
        cv2.imshow("Extracted Pixels", result)

# Load the image
image = cv2.imread('photo_2024.jpg')
cv2.imshow("Image", image)

# Set the mouse callback function
cv2.setMouseCallback("Image", select_pixel)

# Wait until a key is pressed
cv2.waitKey(0)
cv2.destroyAllWindows()
