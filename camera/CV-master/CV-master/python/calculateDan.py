#First we get two sets of (x,y) coordinates, Left Ball and Right Ball
#We have: xL, yL, xR, yR

import math

#Choose Coordinates to Test
#xL=1
#yL=1
#xR=-1
#yR=1

#Angle Calculation
def angle(xL, yL, xR, yR):
    
    #determine if Left or Right

    if yR>yL: #left
        direction = "Left"
        if xR>xL: #0-90
            #angle is between 0 and 90
            m1 = (yR-yL)/(xR-xL) #slope
            rad = math.atan(m1)
            angle = rad*180/math.pi
        elif xR<xL: #>90
            #angle is greater than 90
            m1 = (yR-yL)/(xR-xL) #slope
            rad = math.atan(m1)
            angle1 = rad*180/math.pi
            angle = 180-angle1
        else: 
            #angle is exactly 90
            angle = 90   

    elif yR<yL: #right
        direction = "Right"
        if xR>xL: #0-90
            #angle is between 0 and 90
            m1 = (yR-yL)/(xR-xL) #slope
            rad = math.atan(m1)
            angle = -rad*180/math.pi
        elif xR<xL: #>90
            #angle is greater than 90
            m1 = (yR-yL)/(xR-xL) #slope
            rad = math.atan(m1)
            angle = 180 - rad*180/math.pi
        else:
            #angle is exactly 90
            angle = 90

    else: #horizontal
        angle = 0
        direction = ""
    
    return angle, direction

a, d = angle(xL,yL,xR,yR)
#print(d, float("{0:.2f}".format(a)))
