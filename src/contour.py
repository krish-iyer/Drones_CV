import cv2 as cv 
import numpy as np 
import math

frame = cv.imread('opencv_frame_0.png', cv.IMREAD_COLOR)

hsv = cv.cvtColor(frame, cv.COLOR_RGB2HSV)
h = hsv[:,:,0]
s = hsv[:,:,1]
v = hsv[:,:,2]

l_h = 0
l_s = 70
l_v = 70
u_h = 70
u_s = 255
u_v = 255

green_h  = cv.inRange(h,l_h,u_h)
green_s  = cv.inRange(s,l_s,u_s)
green_v  = cv.inRange(v,l_v,u_v)

ms = cv.bitwise_and(green_h, green_h, mask=green_s)
green = cv.bitwise_and(ms, ms, mask=green_v)


row, col = np.where( green == 255)
    
x1 = np.percentile(row, 25, interpolation = 'midpoint')
x3 = np.percentile(row, 75, interpolation = 'midpoint')

x3_index = np.where(row == x3)
x1_index = np.where(row == x1)

y3_index = (np.median(x3_index))
y1_index = (np.median(x1_index))

y3 = col[int(y3_index)]
y1 = col[int(y1_index)]

dir = y3 - y1

   
if (abs(row[0] - row[np.size(row)-1]) < abs(col[0] - col[np.size(col)-1])) :
        yaw_error = math.degrees(math.atan((y3-y1)/(x3-x1)))
else:
        yaw_error = math.degrees(math.atan((x3-x1)/(y3-y1)))

print(yaw_error)

cv.imshow("frame", green)

cv.waitKey(0)