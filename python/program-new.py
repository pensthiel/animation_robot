#!/usr/bin/python3

# Import necessary libraries
from picamera2 import Picamera2, Preview
import RPi.GPIO as GPIO
import os
import random
import keyboard
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # NEXT FRAME
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # PREVIEW
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # test button
GPIO.setup(18, GPIO.OUT)  # output (LED)  WHITE
GPIO.setup(24, GPIO.OUT)  # RED
GPIO.setup(27, GPIO.OUT)  # YELLOW
GPIO.setup(23, GPIO.OUT)  # GREEN
GPIO.setup(16, GPIO.OUT)  # IR

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




# Start the preview using the QTGL backend
picam2.start_preview(Preview.QTGL)

# Create a preview configuration
preview_config = picam2.create_preview_configuration()

# Configure the camera with the preview configuration
picam2.configure(preview_config)

# Start the camera
picam2.start()

# Wait for 2 seconds to allow the camera to initialize
time.sleep(2)

# Get the initial size for cropping
size = picam2.capture_metadata()['ScalerCrop'][2:]

# Get the full resolution of the camera
full_res = picam2.camera_properties['PixelArraySize']

def save_frame(directory=frames_d, prefix='frame', file_format='jpg'):
    global frame_number, frame_to_display  # Declare both as global
    filename = f"{prefix}_{frame_number}.{file_format}"
    filepath = os.path.join(directory, filename)
    picam2.capture_file(filepath)

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
    
        if keyboard.is_pressed('q'):  
            print('Q to exit')
            break
                  # TEST
        if not GPIO.input(21) or not GPIO.input(17) or keyboard.is_pressed('y'):
            print("next button is LOW (pressed), playing the next frame event as a test")
            LEDS_off()
            time.sleep(1)
            LEDS_on()
            test_button_pressed = True

        if next_button_pressed:
            print("next frame starts")
            screen.fill((255, 255, 255))
            # Capture metadata to sync with the arrival of a new camera frame
            picam2.capture_metadata()
            size = [int(s * zoom) for s in size]
            # Calculate the offset to center the cropped area
            offset = [(r - s) // 2 for r, s in zip(full_res, size)]
            # Set the "ScalerCrop" control with the new offset and size
            picam2.set_controls({"ScalerCrop": offset + size})
            save_frame()

            next_button_pressed = False


   

finally:
    # Release resources
    GPIO.cleanup()
    picam2.stop()
