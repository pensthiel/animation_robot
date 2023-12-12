import cv2
import time
import numpy as np


def detect_color(frame, color):
    """
    Detects a specified color in a frame and returns the masked frame.
    """
    frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower = np.array(color[0:3])
    upper = np.array(color[3:6])

    mask = cv2.inRange(frame_hsv, lower, upper)
    masked_frame = cv2.bitwise_and(frame, frame, mask=mask)

    return masked_frame


def find_contours(masked_frame):
    """
    Finds contours in a masked frame and returns a list of contours.
    """
    frame_gray = cv2.cvtColor(masked_frame, cv2.COLOR_BGR2GRAY)
    frame_blur = cv2.GaussianBlur(frame_gray, (7, 7), 1)
    frame_edges = cv2.Canny(frame_blur, 50, 50)

    contours, _ = cv2.findContours(frame_edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    return contours


def find_shape_center(contour):
    """
    Finds the shape of a contour and returns the number of corners and the bounding rectangle.
    """
    area = cv2.contourArea(contour)

    if area > 50: # and area < 350
        x, y, width, height = cv2.boundingRect(contour)
        center_x, center_y = int(x + (width / 2)), int(y + (height / 2))

        return center_x, center_y

    return None, None


def draw_points(frame, point):
    """
    Draws a point on a frame.
    """
    colors_to_draw = [
        # BLUE
        (255, 0, 0),
        # YELLOW
        (0, 255, 255)]

    cv2.circle(frame, [point[0], point[1]], 10, colors_to_draw[point[2]], cv2.FILLED)


points = [] 

colors_to_detect = [ 
    # BLUE
   [ 80, 167, 0, 132, 255, 255],
    # YELLOW
    [24,86, 194, 65, 234, 255]
]

video_capture = cv2.VideoCapture(0)

width, height = 640, 480
brightness = 0

video_capture.set(3, width)
video_capture.set(4, height)


while True:
    success, frame = video_capture.read()    

    for color in colors_to_detect:
        masked_frame = detect_color(frame, color)
        contours = find_contours(masked_frame)
        for contour in contours:
            x, y = find_shape_center(contour)
            if x is not None or y is not None :
                points.append([x, y, colors_to_detect.index(color)])
    if len(points) != 0:
        for point in points:
            draw_points(frame,point)
    
    frame_h = cv2.flip(frame, 1)

    cv2.imshow("Result", frame_h)
    if cv2.waitKey(1) == ord('q'):
        # quit
        break
    elif cv2.waitKey(1) == ord('c'):
        # clean marker
        points = []

