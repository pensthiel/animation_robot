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
print("picam init")

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
filepath = None
filepath2 = None

# Frame count initialization
frame_number = 0
preview_number = 0


preview_config = picam2.create_preview_configuration()
picam2.configure(preview_config)
picam2.start()
print("picam2 started")

# Wait for 2 seconds to allow the camera to initialize
time.sleep(2)


def save_frame(directory=frames_d, prefix='frame', file_format='jpg'):
    try:
        size = picam2.capture_metadata()['ScalerCrop'][2:]
        full_res = picam2.camera_properties['PixelArraySize']
        picam2.capture_metadata()
        size = [int(s * zoom) for s in size]
        offset = [(r - s) // 2 for r, s in zip(full_res, size)]
        picam2.set_controls({"ScalerCrop": offset + size})
        global frame_number, frame_to_display  # Declare both as global
        filename = f"{prefix}_{frame_number}.{file_format}"
        print(filename)
        filepath = os.path.join(directory, filename)
        print(filepath)
        picam2.capture_file(filepath)
        frame_to_display = filepath
        frame_number += 1
        led_signal()
    except Exception as error:
        print(f"Failed to take and save frame: {error}")

    

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

def led_signal():
    LEDS_off()
    time.sleep(1)
    LEDS_on()

screen.fill((200, 150, 250))
LEDS_on()
try:
    while True:
        pygame.display.flip()


       
        if not debounce(17):
            print("next button pressed")
            next_button_pressed = True
        
        if not debounce(21):
            print("exit button pressed")
            break

        if not debounce(22):
            print("preview button pressed")
            preview_button_pressed = True
        

        if next_button_pressed:
            print("next frame starts")
            try:
                screen.fill((255, 255, 255))
                save_frame()
            except Exception as next_frame_error:
                print(f"couldn't complete save_frame {next_frame_error}")
            try:
                if os.path.exists(frame_to_display):  # Checking for file existence outside the loop can speed things up significantly
                    try:
                        image = pygame.image.load(frame_to_display)
                        scaled_image = pygame.transform.scale(image, width, height)
                        screen.fill((255, 255, 255))
                        screen.blit(scaled_image, (0, 0)) 
                        pygame.display.flip()
                        led_signal()
                    except Exception as load_error:
                        print(f"Failed to load image: {load_error}")
                    
            except Exception as file_error:
                print("Error occurred while loading image.")  # Use error handling to catch and report any issues smoothly.

            next_button_pressed = False

        if preview_button_pressed:
            print("preview starts")
            filepath2 = os.path.join(frames_d, f"frame_{preview_number}.jpg")
            preview_number += 1
            print(filepath2)
            if os.path.exists(filepath2):  # Checking for file existence outside the loop can speed up significantly
                try:
                    if not image is None and not image.get_rect().size == (0, 0):
                        image = pygame.image.load(filepath2)
                        scaled_image = pygame.transform.scale(image, width, height)
                        print(filepath2 + " loaded")
                        screen.blit(scaled_image, (0, 0))
                        print(filepath2 + " displayed")
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
                led_signal()
                print("q to quit")
                break
            
            if event.type == pygame.KEYDOWN and event.key == pygame.K_y:
                print("y key event detected")
                if not y_key_pressed:
                    print("next frame triggered with y key")
                    next_button_pressed = True
                    y_key_pressed = True  # Set the variable to True after the action
                    
                if event.type == pygame.KEYUP and event.key == pygame.K_y:
                    y_key_pressed = False  # Reset the variable when the 'Y' key is released


finally:
    # Release resources
    GPIO.cleanup()
    picam2.stop()
    pygame.quit()
    quit()

