import cv2
import numpy as np

# TrackBars for detection colors
def empty(x):
    pass
cv2.namedWindow("TrackBars",cv2.WINDOW_NORMAL)
cv2.resizeWindow("TrackBars",480,240)
cv2.createTrackbar("Hue Min", "TrackBars",0,179,empty)
cv2.createTrackbar("Hue Max", "TrackBars",179,179,empty)
cv2.createTrackbar("Saturation Min", "TrackBars",0,255,empty)
cv2.createTrackbar("Saturation Max", "TrackBars",255,255,empty)
cv2.createTrackbar("Value Min", "TrackBars",0,255,empty)
cv2.createTrackbar("Value Max", "TrackBars",255,255,empty)




# parameters
width = 640
height = 480
brightness = 0

# read webcam
webcam = cv2.VideoCapture(0)

#set parameters
webcam.set(3,width)
webcam.set(4,height)
webcam.set(10,brightness)

# reading and showing frames
while True:
    # read each frame
    success,frame = webcam.read()
    
    # color detection part
    # convert to hsv
    frameHsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

    # read trackbars
    # first it needs experiment and read from TrackBars
    # we can see these with print
    # at the end we will fix values 
    h_min, s_min, v_min = cv2.getTrackbarPos("Hue Min","TrackBars"),cv2.getTrackbarPos("Saturation Min","TrackBars"),cv2.getTrackbarPos("Value Min","TrackBars")
    h_max, s_max, v_max = cv2.getTrackbarPos("Hue Max","TrackBars"),cv2.getTrackbarPos("Saturation Max","TrackBars"),cv2.getTrackbarPos("Value Max","TrackBars")
    print(h_min, s_min, v_min,h_max, s_max, v_max)
    
    # we can find green, red, etc.
    # ...
    

    # define lower bound
    lower = np.array([
        h_min, s_min, v_min
    ])

    # define upper bound
    upper = np.array([
        h_max, s_max, v_max
    ])

    # build mask
    mask = cv2.inRange(frameHsv,lower,upper)

    # result
    result = cv2.bitwise_and(frame,frame,mask = mask)

    # show
    cv2.imshow("WEBCAM",result)
    if cv2.waitKey(1) == ord('q'):
        break