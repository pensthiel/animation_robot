import cv2
import numpy as np
import pygame
from pygame.locals import QUIT

circle_sensitivity = 50  # adjust this value for circle sensitivity, lower values make it more sensitive
dark_color_sensitivity = 170  # adjust this value for dark color sensitivity

# Initialize Pygame
pygame.init()

# Set display size
screen_size = (0, 0)  # Set to (0, 0) for full screen
screen = pygame.display.set_mode(screen_size, pygame.FULLSCREEN)

# Get the current display info
screen_info = pygame.display.Info()
width = screen_info.current_w
height = screen_info.current_h

x = width
y = height


def detect_dark_color(frame):
    """
    Detects dark colors in a frame.
    """
    frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define the lower and upper bounds for dark colors (black)
    lower_bound = np.array([0, 0, 0])
    upper_bound = np.array([179, 255, dark_color_sensitivity])

    # Create a mask for dark colors
    mask = cv2.inRange(frame_hsv, lower_bound, upper_bound)
    dark_contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    return dark_contours


def draw_circle(frame, center, radius, color):
    """
    Draws a filled circle on the frame.
    """
    cv2.circle(frame, center, radius, color, thickness=cv2.FILLED)

def draw_bordered_rectangle(frame, center, size, border_thickness, color):
    """
    Draws a bordered rectangle on the frame.
    """
    x, y = center
    half_size = int(size / 2)
    cv2.rectangle(frame, (x - half_size, y - half_size), (x + half_size, y + half_size), color, thickness=border_thickness)

# Initialize the camera
cap = cv2.VideoCapture(0)  # Use 0 for the default camera
frame_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
frame_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

# Calculate the ratio
ratio = frame_width / frame_height
new_width = int(height * ratio)

# Circle parameters
circle_radius_small = 20
circle_radius_large = 50

# Rectangle parameters
rectangle_size = min(width, height) - 20  # 20 pixels smaller than the window size
rectangle_border_thickness = 2
rectangle_center = (int(width / 2), int(height / 2))

# Circle positions
circle_center_top_left = (circle_radius_large, circle_radius_large)
circle_center_top_right = (width - circle_radius_large, circle_radius_large)


while True:
    ret, frame = cap.read()
    frame = cv2.resize(frame, (new_width, height))

    # Detect dark colors
    dark_contours = detect_dark_color(frame)

    # Draw a white circle at the top left with adjustable sensitivity
    draw_circle(frame, circle_center_top_left, circle_radius_small, (255, 255, 255))

    # Draw a white circle at the top right with adjustable sensitivity
    draw_circle(frame, circle_center_top_right, circle_radius_small, (255, 255, 255))

    # Draw a bordered rectangle with black borders, centered
    draw_bordered_rectangle(frame, rectangle_center, rectangle_size, rectangle_border_thickness, (0, 0, 0))

    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = pygame.surfarray.make_surface(img.swapaxes(0, 1))
    screen.blit(img, (0, 0))
    pygame.display.flip()
    print("playing video")

    # Check if dark colors are detected inside the circles with adjustable sensitivity
    for contour in dark_contours:
        M = cv2.moments(contour)
        if M["m00"] > 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])

            # Check if inside the top-left circle with adjustable sensitivity
            if circle_center_top_left[0] - circle_sensitivity < cx < circle_center_top_left[0] + circle_sensitivity and \
                    circle_center_top_left[1] - circle_sensitivity < cy < circle_center_top_left[1] + circle_sensitivity:
                draw_circle(frame, circle_center_top_left, circle_radius_small, (0, 0, 255))

            # Check if inside the top-right circle with adjustable sensitivity
            elif circle_center_top_right[0] - circle_sensitivity < cx < circle_center_top_right[0] + circle_sensitivity and \
                    circle_center_top_right[1] - circle_sensitivity < cy < circle_center_top_right[1] + circle_sensitivity:
                draw_circle(frame, circle_center_top_right, circle_radius_small, (0, 0, 255))



    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

    if cv2.waitKey(1) == ord('q'):
        # Quit
        break