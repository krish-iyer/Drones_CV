import numpy as np
import cv2 as cv
import time

def nothing():
    pass

cam = cv.VideoCapture(2)

cam.set(cv.CAP_PROP_FRAME_WIDTH, 1280)
cam.set(cv.CAP_PROP_FRAME_HEIGHT, 720)



cv.namedWindow("Tracking")
cv.createTrackbar("LH", "Tracking", 0,   255, nothing)
cv.createTrackbar("LS", "Tracking", 0,   255, nothing)
cv.createTrackbar("LV", "Tracking", 0,   255, nothing)
cv.createTrackbar("HH", "Tracking", 255, 255, nothing)
cv.createTrackbar("HS", "Tracking", 255, 255, nothing)
cv.createTrackbar("HV", "Tracking", 255, 255, nothing)

#while True:
while(cam.isOpened()):
    ret, frame = cam.read() 
    
    try:
        if ret:
            hsv = cv.cvtColor(frame, cv.COLOR_RGB2HSV)


            h = hsv[:,:,0]
            s = hsv[:,:,1]


            l_h = cv.getTrackbarPos("LH", "Tracking")
            l_s = cv.getTrackbarPos("LS", "Tracking")
            l_v = cv.getTrackbarPos("LV", "Tracking")
            u_h = cv.getTrackbarPos("HH", "Tracking")
            u_s = cv.getTrackbarPos("HS", "Tracking")
            u_v = cv.getTrackbarPos("HV", "Tracking")

            green_h  = cv.inRange(h,l_h,u_h)
            green_s  = cv.inRange(s,l_s,u_s)
            green_v  = cv.inRange(s,l_v,u_v)

            ms = cv.bitwise_and(green_h, green_h, mask=green_s)
            green = cv.bitwise_and(ms, ms, mask=green_v)

            row, col = np.where( green == 255)

            row_avg = np.median(row)
            col_avg = np.median(col)

            print(row_avg, col_avg)
            cv.imshow("image", green)

            cv.imshow("green", frame)

            if cv.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break
    except:
        pass
cam.release()
cv.destroyAllWindows()