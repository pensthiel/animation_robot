#!/usr/bin/python3

# Import necessary libraries
from picamera2 import Picamera2, Preview
import RPi.GPIO as GPIO
import os
import random
import time
import pygame
from pygame.locals import *

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # NEXT FRAME
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # PREVIEW
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # test/quit button
GPIO.setup(18, GPIO.OUT)  # output (LED)  WHITE
GPIO.setup(24, GPIO.OUT)  # RED
GPIO.setup(27, GPIO.OUT)  # YELLOW
GPIO.setup(23, GPIO.OUT)  # GREEN
GPIO.setup(16, GPIO.OUT)  # IR

# Initialize Pygame
pygame.init()
screen_size = (0, 0)  # Set to (0, 0) for full screen
screen = pygame.display.set_mode(screen_size, pygame.FULLSCREEN) # Set display size
screen_info = pygame.display.Info() # Get the current display info
width = screen_info.current_w
height = screen_info.current_h

# Create a Picamera2 instance
picam2 = Picamera2()

zoom = 0.95 # copped image /1

# Set the current working directory to the script's location
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

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
filepath = None
filepath2 = None
# Frame count initialization
frame_number = 0
preview_number = 0





# Create a preview configuration
preview_config = picam2.create_preview_configuration()

# Configure the camera with the preview configuration
picam2.configure(preview_config)

# Start the preview
picam2.start_preview(Preview.DRM)

picam2.start()

# Wait for 2 seconds to allow the camera to initialize
time.sleep(2)

# Get the initial size for cropping
size = picam2.capture_metadata()['ScalerCrop'][2:]

# Get the full resolution of the camera
full_res = picam2.camera_properties['PixelArraySize']

def save_frame(directory=frames_d, prefix='frame', file_format='jpg'):
    screen.fill((255, 255, 255))
    # Capture metadata to sync with the arrival of a new camera frame
    picam2.capture_metadata()
    size = [int(s * zoom) for s in size]
    # Calculate the offset to center the cropped area
    offset = [(r - s) // 2 for r, s in zip(full_res, size)]
    # Set the "ScalerCrop" control with the new offset and size
    picam2.set_controls({"ScalerCrop": offset + size})
    global frame_number, frame_to_display  # Declare both as global
    filename = f"{prefix}_{frame_number}.{file_format}"
    filepath = os.path.join(directory, filename)
    picam2.capture_file(filepath)
    frame_to_display = filepath

def debounce(button_pin):
    time.sleep(0.05)  # Adjust the sleep time based on your requirements
    return GPIO.input(button_pin)

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
    

                  # TEST
        if not debounce(17):
            print("next button is LOW (pressed), playing the next frame event as a test")
            LEDS_off()
            time.sleep(1)
            LEDS_on()
            test_button_pressed = True
        
        if not debounce(21):
            break

        if not debounce(22):
            print("preview button is LOW (pressed), playing the next frame event as a test")
            LEDS_off()
            time.sleep(1)
            LEDS_on()
            preview_button_pressed = True
        

        if next_button_pressed:
            print("next frame starts")
            save_frame()
            picam2.stop_preview()

            try:
                image = pygame.image.load(frame_to_display)
                
                if os.path.exists(filepath):  # Checking for file existence outside the loop can speed things up significantly
                    try:
                        screen.blit(image, (0, 0)) 
                        
                        pygame.display.flip()
                        image_loaded = True
                    except Exception as load_error:
                        print(f"Failed to load image: {load_error}")
                    
            except Exception as file_error:
                print("Error occurred while loading image.")  # Use error handling to catch and report any issues smoothly.

            next_button_pressed = False

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
                        time.sleep(0.1)
                
                except Exception as file_error:
                    print("Error occurred while loading the image.")   # Use error handling to catch and report any issues smoothly.
          
            else:
                print("can't preview: Directory empty")
                preview_button_pressed = False

            if preview_number > frame_number:
                preview_number = 0
                preview_button_pressed = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                print("q to quit")
                break
            
            if event.type == pygame.KEYDOWN and event.key == pygame.K_y:
                print("y key event detected")
                if not y_key_pressed:
                    print("next frame triggered with y key")
                    test_button_pressed = True
                    y_key_pressed = True  # Set the variable to True after the action
                    
                if event.type == pygame.KEYUP and event.key == pygame.K_y:
                    y_key_pressed = False  # Reset the variable when the 'Y' key is released





   

finally:
    # Release resources
    GPIO.cleanup()
    picam2.stop()
    pygame.quit()
    quit()
