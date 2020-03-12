import numpy as np
import cv2 as cv
import time
from MultiWii import MultiWii
import math 
import xlsxwriter

workbook = xlsxwriter.Workbook('Example3.xlsx') 
worksheet = workbook.add_worksheet() 

excl_cnt = 0

def nothing():
    pass

UDP_IP1 = "192.168.43.4"
UDP_PORT1 = 8888

board1 = MultiWii(UDP_IP1, UDP_PORT1)

def yaw_error(row, col):

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
    
    worksheet.write(excl_cnt, 0, yaw_error)
    worksheet.write(excl_cnt, 1, x3)
    worksheet.write(excl_cnt, 2, x1)
    worksheet.write(excl_cnt, 3, dir)

    print(yaw_error)




def drone_cv(excl_cnt):
    try:
        if (cam.isOpened()):
            ret, frame = cam.read() 
                        
            if ret:
                hsv = cv.cvtColor(frame, cv.COLOR_RGB2HSV)
                h = hsv[:,:,0]
                s = hsv[:,:,1]
                v = hsv[:,:,2]

                # l_h = cv.getTrackbarPos("LH", "Tracking")
                # l_s = cv.getTrackbarPos("LS", "Tracking")
                # l_v = cv.getTrackbarPos("LV", "Tracking")
                # u_h = cv.getTrackbarPos("HH", "Tracking")
                # u_s = cv.getTrackbarPos("HS", "Tracking")
                # u_v = cv.getTrackbarPos("HV", "Tracking")
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
                
                # kernel = np.ones((3,3),np.uint8)
                # erosion = cv.erode(green,kernel,iterations = 1)

                
                row, col = np.where( green == 255)

                if (abs(row[0] - row[np.size(row)-1]) < abs(col[0] - col[np.size(col)-1])) :
                    yaw_error(col, row)
                elif (abs(row[0] - row[np.size(row)-1]) > abs(col[0] - col[np.size(col)-1])):
                    yaw_error(row, col)

                cv.imshow("green", green)
    except:
        pass

cam = cv.VideoCapture(2)
cam.set(cv.CAP_PROP_FRAME_WIDTH, 1280)
cam.set(cv.CAP_PROP_FRAME_HEIGHT, 720)
# cv.namedWindow("Tracking")
# cv.createTrackbar("LH", "Tracking", 0,   255, nothing)
# cv.createTrackbar("LS", "Tracking", 0,   255, nothing)
# cv.createTrackbar("LV", "Tracking", 0,   255, nothing)
# cv.createTrackbar("HH", "Tracking", 255, 255, nothing)
# cv.createTrackbar("HS", "Tracking", 255, 255, nothing)
# cv.createTrackbar("HV", "Tracking", 255, 255, nothing)

# board1.arm()

drone_cv(excl_cnt)

board1.send_cmd(board1.MSP["SET_RAW_RC"], board1.channel)

while True:
    try:
        drone_cv(excl_cnt)
        #print(rw - ini_x, cl - ini_y)
        excl_cnt += 1

        # if (abs((rw - ini_x))) > 40:
        # #    board1.channel[2] = 1500
        #     board1.channel[1] = 1500 + int(0.5*(rw-ini_x))
        #     board1.send_cmd(board1.MSP["SET_RAW_RC"], board1.channel)
        
        # elif (abs((cl - ini_y))) > 40:
        # #    board1.channel[2] = 1500
        #     board1.channel[0] = 1500 - int(0.5*(cl-ini_y))
        #     board1.send_cmd(board1.MSP["SET_RAW_RC"], board1.channel)

        # else:
        # #    board1.channel[2] = 1100
        #     board1.channel[0] = 1500
        #     board1.channel[1] = 1500
        #     board1.send_cmd(board1.MSP["SET_RAW_RC"], board1.channel)

        if cv.waitKey(1) & 0xFF == ord('q'):
            board1.disarm()
            workbook.close()
            break
    except:
        pass