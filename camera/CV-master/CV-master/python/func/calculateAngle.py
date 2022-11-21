import math

def angleCalculation(xL, yL, xR, yR):
    #calculate slope and convert to radians
    radiansSlope = math.atan((yR-yL)/(xL-xR))
    #calculate base angle
    angle = radiansSlope*180/math.pi

    #determine if Left or Right
    if yR>yL: #left
        direction = "Left"
        if xL>xR: #0-90 
            #CASE 1L: angle is between 0 and 90
            case = "1L"
            pass
        elif xL<xR: #>90
            #CASE 2L: angle is greater than 90
            angle += 180
            case = "2L"
        else: 
            #angle is exactly 90
            angle = 90   
    elif yR<yL: #right
        direction = "Right"
        if xL>xR: #0-90
            #CASE 1R: angle is between 0 and 90
            angle = -1*angle
            case = "1R"
        elif xL<xR: #>90
            #CASE 2R: angle is greater than 90
            angle = 180 - angle
            case = "2R"
        else:
            #angle is exactly 90
            angle = 90
    else: #horizontal
        angle = 0
        direction = "Horizontal"
    
    return angle, direction