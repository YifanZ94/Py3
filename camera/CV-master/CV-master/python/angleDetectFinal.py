import cv2 as cv
import numpy as np
import math


#Setting the font to be standardized throughout
font = cv.FONT_HERSHEY_SIMPLEX

#Setting the coordinates for calibration line
center_x1 = 25
center_x2 = 175
center_y = 250


def main():

    cap = cv.VideoCapture(0)

    while(1):

        _, frame = cap.read()
        process(frame)

        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()


def process(frame):
    #calling all the methods to eventually calculate the angle
    thresh = normalize(frame)
    contours = contourCalc(thresh, frame)
    cx, cy, cx2, cy2 = centroid(contours, frame)
    midx, midy = midpoint()
    drawing_lines(frame, cx, cy, cx2, cy2, midx, midy)
    #hypotenuse1, horizontal1, vertical1, hypotenuse2, horizontal2, vertical2 = calculate_distance(cx, cy, cx2, cy2, midx, midy)
    #angle1, angle2 = calc_angle(hypotenuse1, horizontal1, vertical1, hypotenuse2, horizontal2, vertical2)
    #angleText(angle1, angle2, frame)

<<<<<<< HEAD
    #Show the final frame
=======
    #Show the final frames
>>>>>>> e5f28fd191a9ad48fad31918a569f8c5dbd3225e

    cv.imshow("Angle Detection", frame)


#Blur the inputted image feed, mask the image so the background is black and anything in between the 
#high and low HSV values are turned to white. Dilate the masked image to get defined lines. Add a 
#threshold to get rid of noise in the image. Return image feed after normalization.
def normalize(frame):

    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    blur = cv.GaussianBlur(hsv, (5, 5), 0)

    #lowerGreen = np.array([20, 50, 50])
    #upperGreen = np.array([40, 255, 255])

    lowerGreen = np.array([20, 70, 70])
    upperGreen = np.array([40, 255, 255])

    maskGreen = cv.inRange(hsv, lowerGreen, upperGreen)

    kernel = np.ones((5, 5), np.uint8)
    dilate = cv.dilate(maskGreen, kernel, iterations=2)

    ret, thresh = cv.threshold(dilate, 15, 275, cv.THRESH_BINARY)

    return thresh


#Send in the normalized image feed and the untouched image feed. Calculate the contours in the image
#using the normalized image. This is returning back all points that create a boundary of an object 
#in the image. Draw those contours around the object in green and return the list of contours.
def contourCalc(thresh, frame):

<<<<<<< HEAD
    images, contours, hierarchy = cv.findContours(thresh, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
=======
    contours, hierarchy = cv.findContours(thresh, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
>>>>>>> e5f28fd191a9ad48fad31918a569f8c5dbd3225e
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
    #cv.line(frame, (cx, cy), (midx, midy), (0, 0, 255), 3)
    #cv.line(frame, (cx2, cy2), (midx, midy), (0, 255, 0), 3)
    
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

    arcSinVal1 = vertical1/hypotenuse1
    arcSinVal2 = vertical2/hypotenuse2

    angle1 = np.arcsin(arcSinVal1)*180/math.pi
    angle2 = np.arcsin(arcSinVal2)*180/math.pi

    return angle1, angle2
    
    
def angleText(angle1, angle2, frame):
    angle1_text = str(int(angle1))
    angle2_text = str(int(angle2))

    #cv.putText(frame, angle1_text, (), font, 1, (213, 38, 181), 2)
    #cv.putText(frame, angle2_text, (), font, 1, (222, 100, 8), 2)
    

#run program
main()


