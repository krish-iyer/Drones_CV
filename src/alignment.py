import cv2 as cv 
import numpy as np 

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

kernel = np.ones((3,3),np.uint8)
erosion = cv.erode(green,kernel,iterations = 1)

row, col = np.where( erosion == 255)
if (abs(row[0] - row[np.size(row)-1]) < abs(col[0] - col[np.size(col)-1])) :
    tmp = row
    row = col
    col = tmp
    
x1 = np.percentile(row, 25, interpolation = 'midpoint')
x3 = np.percentile(row, 75, interpolation = 'midpoint')
x3_index = np.where(row == x3)
x1_index = np.where(row == x1)
y3_index = (np.median(x3_index))
y1_index = (np.median(x1_index))
y3 = col[int(y3_index)]
y1 = col[int(y1_index)]
dir = y3 - y1
yaw_error = abs(x3-x1)


# col_in_y3 = np.where( row == y3 )
# x3 = int((np.size(col_in_y3) - 1)/2)
# Q3 = col[x3]

# col_in_y1 = np.where( row == y1 )
# x1 = int((np.size(col_in_y1) - 1)/2)
# Q1 = row[x1]

print(y3-y1)

cv.imshow("frame", erosion)

cv.waitKey(0)

# row_avg = np.median(row)
# col_avg = np.median(col)

# y1 = np.percentile(col, 25, interpolation = 'midpoint')
# y3 = np.percentile(col, 75, interpolation = 'midpoint')

# col_in_y3 = np.where( col == y3 )
# row_val_y3 = row[col_in_y3]

# col_in_y1 = np.where( col == y1 )
# row_val_y1 = row[col_in_y1]

# x3 = np.average(row_val_y3)
# x1 = np.average(row_val_y1)
# yaw_error = x3 - x1

# print(yaw_error)
