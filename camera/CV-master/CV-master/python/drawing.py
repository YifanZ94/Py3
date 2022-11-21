import numpy as np
import cv2 as cv

cap = cv.VideoCapture(0)

#setting the font
font = cv.FONT_HERSHEY_SIMPLEX

while(1):

    
    _, frame = cap.read()

    #draw a diagonal blue line with a thickness of 5 px
    #parameters: input, starting coordinates, ending coordinates, color, thickness
    #origin is top left of frame
    line_frame = cv.line(frame, (0, 0), (511, 511), (255, 0, 0), 5)

    #draw a circle that is filled in (hence -1) 
    #parameters: input, center coordinates, radius, color, filled in or not filled in
    circle_frame = cv.circle(frame, (447, 63), 63, (0, 0, 255), -1)

    #parameters: input, text, position coordinates, font, font scale, color, thickness, lineType
    cv.putText(line_frame, "OpenCV blue line", (10, 500), font, 4, (255, 255, 255), 2, cv.LINE_AA)

    cv.imshow("Line", line_frame)
    cv.imshow("Circle", circle_frame)

    k = cv.waitKey(5) & 0xff

    if k == 27:
        break

cv.destroyAllWindows()

