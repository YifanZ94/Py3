#!/usr/bin/python3

import cv2 as cv
import numpy as np
import math
import tkinter as tk

#Setting the font to be standardized throughout
font = cv.FONT_HERSHEY_SIMPLEX

#Setting the coordinates for calibration line
center_x1 = 25
center_x2 = 175
center_y = 250

class App:
     def __init__(self, window, window_title, video_source=0):
         self.window = window
         self.window.title("Angle Detection")
         self.video_source = video_source
 
         # open video source (by default this will try to open the computer webcam)
         self.vid = MyVideoCapture(self.video_source)
 
         # Create a canvas that can fit the above video source size
         self.canvas = tkinter.Canvas(window, width = self.vid.width, height = self.vid.height)
         self.canvas.pack()
 
         # After it is called once, the update method will be automatically called every delay milliseconds
         self.delay = 15
         self.update()
 
         self.window.mainloop()
 
 
     def update(self):
         # Get a frame from the video source
         ret, frame = self.vid.get_frame()
 
         if ret:
             self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
             self.canvas.create_image(0, 0, image = self.photo, anchor = tkinter.NW)
 
         self.window.after(self.delay, self.update)
 

class MyVideoCapture:
    def __init__(self, video_source=0):
        # Open the video source
        self.vid = cv.VideoCapture(0)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", 0)
 
        while(1):
            _, frame = self.vid.read()
            process(frame)

            if cv.waitKey(1) & 0xFF == ord('q'):
                break

        self.vid.release()
        cv.destroyAllWindows()

    def process(frame):
        #calling all the methods to eventually calculate the angle
        thresh = normalize(frame)
        contours = contourCalc(thresh, frame)
        cx, cy, cx2, cy2 = centroid(contours, frame)
        midx, midy = midpoint()
        drawing_lines(frame, cx, cy, cx2, cy2, midx, midy)
        hypotenuse1, horizontal1, vertical1, hypotenuse2, horizontal2, vertical2 = calculate_distance(cx, cy, cx2, cy2, midx, midy)
        angle1, angle2 = calc_angle(hypotenuse1, horizontal1, vertical1, hypotenuse2, horizontal2, vertical2)
        angleText(angle1, angle2, frame)

        #Show the final frame

        frame.set(cv.CV_CAP_PROP_FRAME_WIDTH, 600)
        frame.set(cv.CV_CAP_PROP_FRAME_HEIGHT, 480)

        cv.imshow("Angle Detection", frame)

    #Blur the inputted image feed, mask the image so the background is black and anything in between the 
    #high and low HSV values are turned to white. Dilate the masked image to get defined lines. Add a 
    #threshold to get rid of noise in the image. Return image feed after normalization.
    def normalize(frame):

        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        blur = cv.GaussianBlur(hsv, (5, 5), 0)

        lowerGreen = np.array([20, 50, 50])
        upperGreen = np.array([40, 255, 255])

        maskGreen = cv.inRange(hsv, lowerGreen, upperGreen)

        kernel = np.ones((5, 5), np.uint8)
        dilate = cv.dilate(maskGreen, kernel, iterations=2)

        ret, thresh = cv.threshold(dilate, 15, 255, cv.THRESH_BINARY)

        return thresh


    #Send in the normalized image feed and the untouched image feed. Calculate the contours in the image
    #using the normalized image. This is returning back all points that create a boundary of an object 
    #in the image. Draw those contours around the object in green and return the list of contours.
    def contourCalc(thresh, frame):

        _, contours, _ = cv.findContours(thresh, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
        cv.drawContours(frame, contours, -1, (0, 255, 0), 3)
        return contours


    #Send in the list of contours calculated from contourCalc and the untouched image feed. Here, we are
    #calculating centroid by using the moments method. 
    def centroid(contours, frame):
        if len(contours) > 0:
            #outputs a dictionary of all moments calculated like area, centroid, etc
            
            #TENNIS BALL 1 Centroid
            M = cv.moments(contours[0])

            if M['m00'] > 0:
                #calculation of centroid
                cx = int(M['m10'] / M['m00'])
                cy = int(M['m01'] / M['m00'])
                #draw centroid
                centroid = cv.circle(frame, (cx, cy), 5, (0, 0, 255), -1)
                cv.putText(frame, "Centroid", (cx - 25, cy -25), font, 1, (255, 255, 255), 2, cv.LINE_AA)
                
            else:
                #draw centroids off the screen
                cx, cy = 700, 700
            
            #if another object is detected with centroid (aka TENNIS BALL 2)
            if len(contours) > 1:

                #TENNIS BALL 2 Centroid
                M = cv.moments(contours[1])

                if M['m00'] > 0:
                
                    cx2 = int(M['m10'] / M['m00'])
                    cy2 = int(M['m01'] / M['m00'])
                    centroid = cv.circle(frame, (cx2, cy2), 5, (0, 0, 255), -1)
                    cv.putText(frame, "Centroid2", (cx2 - 25, cy2 -25), font, 1, (255, 255, 255), 2, cv.LINE_AA)
                    
                else:
                    cx2, cy2 = 700, 700
            else: 
                cx2, cy2 = 700, 700
        else:
            cx, cy = 700, 700
            cx2, cy2 = 700, 700

        return cx, cy, cx2, cy2


    #Midpoint calucaltion of the calibration line
    def midpoint():
        midx = (center_x1 + center_x2) / 2
        midy = (center_y + center_y) / 2

        return midx, midy   


    #Draw lines to connect the centroids of both tennis balls to eachother, to the midpoint of the calibration line,
    #and draw the calibration line. 
    def drawing_lines(frame, cx, cy, cx2, cy2, midx, midy):

        #draw calibration line
        cv.line(frame, (center_x1, center_y), (center_x2, center_y), (130, 40, 230), 3)

        #draw line connecting the two centroids together
        #cv.line(frame, (cx, cy), (cx2, cy2), (255, 0 , 0), 5)

        #draw a line from each centroid to connect to the center. 
        cv.line(frame, (cx, cy), (midx, midy), (0, 0, 255), 3)
        cv.line(frame, (cx2, cy2), (midx, midy), (0, 255, 0), 3)
        
        #draw a line to create a triangle (keep for testing angle for now)
        #cv.line(frame, (cx, cy), (center_x1, center_y), (140, 230, 60), 2)
        #cv.line(frame, (cx2, cy2), (center_x2, center_y), (140, 230, 60), 2)    


    #Helper distance method for calculate_distance method
    def distance(x1, x2, y1, y2):
        distance = math.sqrt( ((x2-x1)**2)+((y2-y1)**2) )
        return distance


    #Calculate the distance of the lines created and returning their lengths
    def calculate_distance(cx, cy, cx2, cy2, midx, midy):
        #find the distance of each of the lines for both triangles
        hypotenuse1 = distance(cx, midx, cy, midy)
        horizontal1 = distance(center_x1, midx, center_y, midy)
        vertical1 = distance(cx, center_x1, cy, center_y)

        hypotenuse2 = distance(cx2, midx, cy2, midy)
        horizontal2 = distance(center_x2, midx, center_y, midy)
        vertical2 = distance(cx2, center_x2, cy2, center_y)

        return hypotenuse1, horizontal1, vertical1, hypotenuse2, horizontal2, vertical2


    #Calculating the angles using arcsin
    def calc_angle(hypotenuse1, horizontal1, vertical1, hypotenuse2, horizontal2, vertical2):

        angle1 = np.arcsin(vertical1/hypotenuse1)*180/math.pi
        angle2 = np.arcsin(vertical2/hypotenuse2)*180/math.pi

        return angle1, angle2


    def angleText(angle1, angle2, frame):
        angle1_text = str(int(angle1))
        angle2_text = str(int(angle2))

        cv.putText(frame, angle1_text, (), font, 1, (213, 38, 181), 2)
        cv.putText(frame, angle2_text, (), font, 1, (222, 100, 8), 2)

    # Release the video source when the object is destroyed
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()
        self.window.mainloop()

#run program
main()