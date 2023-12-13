import cv2
import pygame
from pygame.locals import *
import os

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

# Function to capture and return a frame from the camera
def capture_frame():
    ret, frame = cap.read()
    if ret:
        frame = cv2.resize(frame, (new_width, height))
        return frame
    else:
        print("Failed to capture frame")
        return None

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
            frame = capture_frame()
            if frame is not None:
                img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = pygame.surfarray.make_surface(img.swapaxes(0, 1))
                screen.blit(img, (0, 0))
                pygame.display.flip()

        # Handle events
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_q):
                raise StopIteration  # Break out of the loop

            # Check for 'y' key press to save the frame
            if event.type == KEYDOWN and event.key == K_y:
                frame = capture_frame()
                if frame is not None:
                    save_frame(frame)  # Save the frame with an auto-incremented number
                    store_frame(frame)  # Save the preview frame with a fixed name

except StopIteration:
    pass  # Exit the loop when 'q' is pressed or the window is closed

finally:
    # Release resources
    pygame.quit()
    cap.release()