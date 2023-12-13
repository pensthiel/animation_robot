import cv2
import pygame
from pygame.locals import *

# Initialize Pygame
pygame.init()

# Set display size
screen_size = (0, 0)  # Set to (0, 0) for full screen
screen = pygame.display.set_mode(screen_size, FULLSCREEN)

# Get the current display info
screen_info = pygame.display.Info()
width = (screen_info.current_w)
height = (screen_info.current_h)

# Initialize the camera
cap = cv2.VideoCapture(0)  # Use 0 for the default camera

# Fetch the frame width and height
frame_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
frame_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

# Calculate the ratio
ratio = frame_width / frame_height
new_width = int(height * ratio) 

try:
    while True:
        ret, frame = cap.read()
        frame = cv2.resize(frame, ( new_width, height))
        if not ret:
            print("Error capturing the frame.")
            break

        # Convert the OpenCV frame to Pygame surface
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = pygame.surfarray.make_surface(img.swapaxes(0, 1))

        # Display the image on the screen
        screen.blit(img, (0, 0))
        pygame.display.flip()

        # Handle events
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_q):
                pygame.quit()
                cap.release()
                exit()

            # Check for 'q' key press
            keys = pygame.key.get_pressed()
            if keys[K_q]:
                pygame.quit()
                cap.release()
                exit()

finally:
    # Release resources
    cap.release()

