import cv2
import pygame
from pygame.locals import *
import os
import time

# Set the current working directory to the script's location
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# Initialize Pygame
pygame.init()

# Set display size
screen_size = (0, 0)  # Set to (0, 0) for full screen
screen = pygame.display.set_mode(screen_size, pygame.FULLSCREEN)

# Get the current display info
screen_info = pygame.display.Info()
width = screen_info.current_w
height = screen_info.current_h

# Initialize the camera
cap = cv2.VideoCapture(0)  # Use 0 for the default camera

# Fetch the frame width and height
frame_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
frame_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

# Calculate the ratio
ratio = frame_width / frame_height
new_width = int(height * ratio)

# Frame count initialization
frame_number = 0

# Create 'frames' directory if it doesn't exist
if not os.path.exists('frames'):
    os.makedirs('frames')

# Function to save the frame
def save_frame(image, directory='frames', prefix='frame', file_format='jpg'):
    global frame_number  # Declare frame_number as global to modify it
    filename = f"{prefix}_{frame_number}.{file_format}"
    filepath = os.path.join(directory, filename)
    cv2.imwrite(filepath, image)
    print(f"Saved: {filepath}")
    frame_number += 1  # Increment the frame number

# Function to store the preview frame
def store_frame(image, prefix='preview_frame', file_format='jpg'):
    filename = f"{prefix}.{file_format}"  # Corrected line
    cv2.imwrite(filename, image)
    print(f"Saved: {filename}")

def play_vid(frame):
    frame = cv2.resize(frame, (new_width, height))
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = pygame.surfarray.make_surface(img.swapaxes(0, 1))
    screen.blit(img, (0, 0))
    pygame.display.flip()

try:
    while True:
        
        # Attempt to load the image
        image_path = 'preview_frame.jpg'
        image_loaded = False
        if os.path.exists(image_path):
            try:
                image = pygame.image.load(image_path)
                image = pygame.transform.scale(image, (new_width, height))
                screen.blit(image, (0, 0))
                pygame.display.flip()
                image_loaded = True
            except Exception as e:
                print(f"Failed to load image: {e}")

        # If the image is not loaded, capture a new frame
        if not image_loaded:
            ret, frame = cap.read()
            if frame is not None:
                play_vid()

        # Handle events
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_q):
                raise StopIteration  # Break out of the loop

            # Check for 'y' key press to save the frame
            if event.type == KEYDOWN and event.key == K_y:
                ret, frame = cap.read()
                play_vid(frame)
                save_frame(frame)  # Save the frame with an auto-incremented number
                store_frame(frame)  # Save the preview frame with a fixed name
                time.sleep(3)  # Adds a delay of 'number_of_seconds'
                

except StopIteration:
    pass  # Exit the loop when 'q' is pressed or the window is closed

finally:
    # Release resources
    pygame.quit()
    cap.release()