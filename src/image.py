import numpy as np
import cv2 as cv

frame = cv.imread("rgb.jpg")

hsv = cv.cvtColor(frame, cv.COLOR_RGB2HSV)


h = hsv[:,:,0]

#h_th = np.where(h < 60,1,0)

green  = cv.inRange(h,60,80)
red   = cv.inRange(h, 120, 150)  
blue   = cv.inRange(h, 0, 10)  

ret, count = np.unique(green)

row, col = np.where( green == 255)

row_avg = np.median(row)
col_avg = np.median(col)

print(row_avg, col_avg)

cv.imshow("green", green)
cv.imshow("red", red)
cv.imshow("blue", blue)

#print(h_th)

#print(s)


# brightest = y.max()
# threshold = brightest / 2

# th = np.where(y>threshold,255,0)

# cv.imshow("titl", th)

# print(brightest)
#print(frame[:,:,1])
cv.waitKey(0)