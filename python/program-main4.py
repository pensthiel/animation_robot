import cv2
import pygame
from pygame.locals import *
import RPi.GPIO as GPIO
import os
import random
from picamera2 import Picamera2, Preview
from signal import pause


GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # NEXT FRAME
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # PREVIEW
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # test button
GPIO.setup(18, GPIO.OUT)  # output (LED)  WHITE
GPIO.setup(24, GPIO.OUT)  # RED
GPIO.setup(27, GPIO.OUT)  # YELLOW
GPIO.setup(23, GPIO.OUT)  # GREEN
GPIO.setup(16, GPIO.OUT)  # IR

# Initialize Pygame
pygame.init()

# how much time we give the pi to save the image
SaveDelay = 2000  # 2 seconds in milliseconds
VidFrameRate = 100

# Use Pygame's clock to handle the timing
clock = pygame.time.Clock()
start_ticks = pygame.time.get_ticks()  # Starter tick

# Set the current working directory to the script's location
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# Set display size
screen_size = (0, 0)  # Set to (0, 0) for full screen
screen = pygame.display.set_mode(screen_size, pygame.FULLSCREEN)

# Get the current display info
screen_info = pygame.display.Info()
width = screen_info.current_w
height = screen_info.current_h

# Initialize the camera
picam2 = Picamera2()
picam2.preview_configuration.main.size = (width, height)
picam2.preview_configuration.main.format = "RGB888"
picam2.preview_configuration.align()
picam2.configure("preview")
picam2.start()
print("picam2 Initialized")

# Frame count initialization
frame_number = 0
preview_number = 0

# Generate a random integer from 1 to 1000
rand_int = random.randint(1, 1000)
print(f"Random integer between 1 and 1000: {rand_int}")

# Create 'frames' directory if it doesn't exist
os.makedirs(f"frames{rand_int}")
frames_d = (f"frames{rand_int}")

y_key_pressed = False
frame_to_display = None
next_button_pressed = False
preview_button_pressed = False
test_button_pressed = False
filepath2 = None


# Function to save the frame
def save_frame(directory=frames_d, prefix='frame', file_format='jpg'):
    global frame_number, frame_to_display  # Declare both as global
    filename = f"{prefix}_{frame_number}.{file_format}"
    filepath = os.path.join(directory, filename)
    
    try:
        with picam2.capture_file("still", filepath) as f:  # Use 'with open()' to ensure proper file handling
            print(f"{filepath} Saved")
            
        frame_to_display = filepath
        
        frame_number += 1  # Increment the frame number
    except Exception as save_error:
        print(f"Error saving frame: {save_error}")


def delay():
    save_delay_ticks = SaveDelay
    start_save_delay_ticks = pygame.time.get_ticks()
    while pygame.time.get_ticks() - start_save_delay_ticks < save_delay_ticks:
        clock.tick(60)

def LEDS_on():
    GPIO.output(18, GPIO.HIGH)
    GPIO.output(24, GPIO.HIGH)
    GPIO.output(27, GPIO.HIGH)
    GPIO.output(23, GPIO.HIGH)

def LEDS_off():
    GPIO.output(18, GPIO.LOW)
    GPIO.output(24, GPIO.LOW)
    GPIO.output(27, GPIO.LOW)
    GPIO.output(23, GPIO.LOW)

LEDS_on()

try:
    while True:
        seconds = (pygame.time.get_ticks() - start_ticks) / 1000
        image_loaded = False
        frame = picam2.capture_array()

        # TEST
        if not GPIO.input(21):
            print("test button is LOW (pressed), playing the next frame event as a test")
            test_button_pressed = True

        # NEXT BUTTON
        if not GPIO.input(17):  # if port 17 == 0
            print("next frame button is LOW (pressed)")
            next_button_pressed = True

        # PREVIEW
        if not GPIO.input(22):
            print("preview button is LOW (pressed)")
            preview_button_pressed = True

        if test_button_pressed:
            cv2.imshow("Camera", frame)
            print("cv2.imshow(Camera, frame)")



        if next_button_pressed:
            print("next frame starts")
            screen.fill((255, 255, 255))
            try:
                cv2.imshow("Camera", frame)
                save_frame(frame)  # Save the frame with an auto-incremented number

            except Exception as display_error:
                print(f"Error while trying to show the camera feed or update display: {display_error}")
                next_button_pressed = False

            # Delay before loading and displaying the image
            delay()

            # DISPLAY IMAGE
            try:
                image = pygame.image.load(frame_to_display)
                
                if os.path.exists(filepath2):  # Checking for file existence outside the loop can speed things up significantly
                    try:
                        screen.blit(image, (0, 0))
                        
                        pygame.display.flip()
                        image_loaded = True
                    except Exception as load_error:
                        print(f"Failed to load image: {load_error}")
                    
            except Exception as file_error:
                print("Error occurred while loading image.")  # Use error handling to catch and report any issues smoothly.


            # Delay before you can press the button again
            delay()
            next_button_pressed = False  # Set the variable to True after the action

        # PREVIEW
        if preview_button_pressed:
            print("preview starts")
            filepath2 = os.path.join(frames_d, f"frame{preview_number}.jpg")
            if os.path.exists(filepath2):  # Checking for file existence outside the loop can speed up significantly
                try:
                    image = pygame.image.load(filepath2)
                    print(filepath2 + " loaded")
                    if not image is None and not image.get_rect().size == (0, 0):
                        screen.blit(image, (0, 0))
                        print(filepath2 + " displayed")
                        pygame.display.flip()
                        image_loaded = True
                        preview_number += 1

                        VidFrameRate_ticks = VidFrameRate
                        start_VidFrameRate_ticks = pygame.time.get_ticks()
                        while pygame.time.get_ticks() - start_VidFrameRate_ticks < VidFrameRate_ticks:
                            clock.tick(60)
                
                except Exception as file_error:
                    print("Error occurred while loading the image.")   # Use error handling to catch and report any issues smoothly.
          
            else:
                print("can't preview: Directory empty")
                preview_button_pressed = False

            if preview_number > frame_number:
                preview_number = 0
                preview_button_pressed = False

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                print("q to quit")
                pygame.quit()
                cv2.destroyAllWindows()
                break  # Exit the loop on quit event

            # Check for 'y' key press to save the frame
            if event.type == pygame.KEYDOWN and event.key == pygame.K_y:
                print("key event detected")
                if not y_key_pressed:  # Check if the 'Y' key was not already pressed
                    screen.fill((255, 255, 255))
                    pygame.display.flip()  # Ensure the screen updates before capturing the frame
                    save_frame()  # Save the frame with an auto-incremented number

                    # Delay before loading and displaying the image
                    delay()
                    

                    try:
                        image = pygame.image.load(frame_to_display)
                        print(frame_to_display + " loaded")
                        image = pygame.transform.scale(image, (new_width, height))
                        screen.blit(image, (0, 0))
                        pygame.display.flip()
                        image_loaded = True
                        print(frame_to_display + " displayed")
                    except Exception as load_error:
                        print(f"Failed to load image: {load_error}")

                    y_key_pressed = True  # Set the variable to True after the action

            if event.type == pygame.KEYUP and event.key == pygame.K_y:
                y_key_pressed = False  # Reset the variable when the 'Y' key is released



finally:
    # Release resourcesc
    GPIO.cleanup()
    picam2.stop()
    pygame.quit()
    cv2.destroyAllWindows()

