#!/usr/bin/python3

# Import necessary libraries
from picamera2 import Picamera2, Preview
import RPi.GPIO as GPIO
import os
import time
import pygame
from pygame.locals import *



zoom = 0.75 # copped image /1
offset_tweak_left = 160  # Change this value as needed
offset_tweak_top = -120  # Change this value as needed

exp = 13800
gain = 2.5
focus = 1
red = 2.1
blue = 2.1

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # NEXT FRAME
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # PREVIEW
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # test/quit button
GPIO.setup(18, GPIO.OUT)  # output (LED)  WHITE
GPIO.setup(24, GPIO.OUT)  # RED
GPIO.setup(27, GPIO.OUT)  # YELLOW
GPIO.setup(23, GPIO.OUT)  # GREEN
GPIO.setup(26, GPIO.OUT)  # big yellow
GPIO.setup(16, GPIO.OUT)  # IR

pygame.mixer.pre_init()
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



# Set the current working directory to the script's location
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# NUMBER OF FILES IN THE "RELOAD" FOLDER
reload_folder = os.path.join(script_dir, "reload")
frame_number = 0

for root_dir, cur_dir, files in os.walk(reload_folder):
    frame_number += len(files)
    frame_number -= 1

print('File count in', reload_folder, ':', frame_number)

bell = pygame.mixer.Sound("samples/bell.mp3")
music = pygame.mixer.Sound("samples/music.mp3")
#pygame.mixer.Sound.play(bell)
#pygame.mixer.music.stop()
print("bell sound file path:", os.path.abspath("samples/bell.mp3"))
print("music sound file path:", os.path.abspath("samples/music.mp3"))
#pygame.mixer.Sound.play(music)
#pygame.mixer.music.stop()



y_key_pressed = False
w_key_pressed = False
a_key_pressed = False
s_key_pressed = False
d_key_pressed = False
frame_to_display = None
next_button_pressed = False
preview_button_pressed = False
filepath = None
filepath2 = None

# Frame count initialization

preview_number = 0


preview_config = picam2.create_preview_configuration()
picam2.configure(preview_config)
picam2.start()
print("picam2 started")
# Wait for 2 seconds to allow the camera to initialize
time.sleep(2)


picam2.capture_metadata()
size = picam2.capture_metadata()['ScalerCrop'][2:]
full_res = picam2.camera_properties['PixelArraySize']
picam2.capture_metadata()
size = [int(s * zoom) for s in size]
#offset = [(r - s) // 2 for r, s in zip(full_res, size)]
#picam2.set_controls({"ScalerCrop": offset + size})

# Calculate offset based on the initial values
offset_width = (full_res[0] - size[0]) // 2 + offset_tweak_left
offset_height = (full_res[1] - size[1]) // 2 + offset_tweak_top

# Create a list with the individual offset values
offset = [offset_width, offset_height]
print(f"offset : {offset}")
metadata = picam2.capture_metadata()
controls = {c: metadata[c] for c in ["ExposureTime", "AnalogueGain", "ColourGains","ColourTemperature","LensPosition"]}
print(controls)
# Set controls with individual offset values
picam2.set_controls({"AwbEnable": 0})
picam2.set_controls({"ScalerCrop": offset + size,"ExposureTime": exp, "AnalogueGain": gain,"AfMode": 0, "LensPosition": focus,"ColourGains": (red, blue)})








def save_frame(prefix='frame', file_format='jpg'):
    try:
        global frame_number, frame_to_display  # Declare both as global
        filename = f"{prefix}_{frame_number}.{file_format}"
        print(filename)
        filepath = os.path.join("reload", filename)
        print(filepath)

        # Fill the screen with a white background
        screen.fill((255, 255, 255))
        pygame.display.flip()  # Update the display
        time.sleep(0.1)
        picam2.capture_metadata()
        screen.fill((255, 255, 255))
        pygame.display.flip()  # Update the display a second time
        time.sleep(0.1)
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
    GPIO.output(26, GPIO.HIGH)

def LEDS_off():
    GPIO.output(18, GPIO.LOW)
    GPIO.output(24, GPIO.LOW)
    GPIO.output(27, GPIO.LOW)
    GPIO.output(23, GPIO.LOW)
    GPIO.output(26, GPIO.LOW)

def led_signal():
    LEDS_off()
    time.sleep(0.05)
    LEDS_on()


screen.fill((200, 150, 250))
LEDS_on()
try:
    filename = f"frame_{frame_number}.jpg"
    print(filename)
    filepath = os.path.join("reload", filename)
    print(filepath)
    image = pygame.image.load(filepath)
    scaled_image = pygame.transform.scale(image, (width, height))
    screen.blit(scaled_image, (0, 0))
    pygame.display.flip()


except Exception as load_error:
    print(f"Failed to load image: {load_error}")
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
                pygame.mixer.Sound.play(bell)
            except Exception as e:
                print("Error playing sound:", e)
            try:
                save_frame()
            except Exception as next_frame_error:
                print(f"couldn't complete save_frame {next_frame_error}")
            try:
                if os.path.exists(frame_to_display):  # Checking for file existence outside the loop can speed things up significantly
                    try:
                        image = pygame.image.load(frame_to_display)
                        scaled_image = pygame.transform.scale(image, (width, height))
                        screen.blit(scaled_image, (0, 0))
                        pygame.display.flip()


                    except Exception as load_error:
                        print(f"Failed to load image: {load_error}")

            except Exception as file_error:
                print("Error occurred while loading image.")  # Use error handling to catch and report any issues smoothly.

            led_signal()
            next_button_pressed = False

        if preview_button_pressed:
            print("preview starts")
            try:
                pygame.mixer.Sound.play(music)
            except Exception as e:
                print("Error playing sound:", e)
            filepath2 = os.path.join("reload", f"frame_{preview_number}.jpg")
            preview_number += 1
            print(filepath2)
            if os.path.exists(filepath2):  # Checking for file existence outside the loop can speed up significantly
                try:
                    if not image is None and not image.get_rect().size == (0, 0):
                        image = pygame.image.load(filepath2)
                        scaled_image = pygame.transform.scale(image, (width, height))
                        print(filepath2 + " loaded")
                        screen.blit(scaled_image, (0, 0))
                        print(filepath2 + " displayed")
                        time.sleep(0.1)

                except Exception as file_error:
                    print("Error occurred while loading the image.")   # Use error handling to catch and report any issues smoothly.

            else:
                print("can't preview: Directory empty")
                preview_button_pressed = False
            try:
                if preview_number == frame_number:
                    preview_number = 0
                    pygame.mixer.stop()
                    preview_button_pressed = False
            except Exception as e:
                print(f"error stopping preview: {e}")

            if preview_number == 5000:
                preview_number = 0
                pygame.mixer.stop()
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

            if event.type == pygame.KEYDOWN and event.key == pygame.K_w:
                if not w_key_pressed:
                    print("up")
                    #offset_tweak_left = 320  # Change this value as needed
                    offset_tweak_top += 2

                    print(f": {offset_tweak_top}")
                    w_key_pressed = True  # Set the variable to True after the actio
                if event.type == pygame.KEYUP and event.key == pygame.K_w:
                    w_key_pressed = False  # Reset the variable when the 'Y' key is released

            if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
                if not a_key_pressed:
                    print("left")
                    offset_tweak_left += 2  # Change this value as needed

                    print(f"left: {offset_tweak_left}")
                    a_key_pressed = True  # Set the variable to True after the actio
                if event.type == pygame.KEYUP and event.key == pygame.K_a:
                    a_key_pressed = False  # Reset the variable when the 'Y' key is released

            if event.type == pygame.KEYDOWN and event.key == pygame.K_d:
                if not d_key_pressed:
                    print("right")
                    offset_tweak_left -= 2 # Change this value

                    print(f"left: {offset_tweak_left}")
                    d_key_pressed = True  # Set the variable to True after the actio
                if event.type == pygame.KEYUP and event.key == pygame.K_d:
                    d_key_pressed = False  # Reset the variable when the 'Y' key is released

            if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                if not s_key_pressed:
                    print("down")
                    #offset_tweak_left -= 2 # Change this value
                    offset_tweak_top -= 2

                    print(offset_tweak_top)
                    s_key_pressed = True  # Set the variable to True after the actio
                if event.type == pygame.KEYUP and event.key == pygame.K_s:
                    s_key_pressed = False  # Reset the variable when the 'Y' key is released


except KeyboardInterrupt:
    pass  # Handle the Ctrl+C interrupt to gracefully exit the program


finally:
    # Release resources
    pygame.mixer.quit()
    GPIO.cleanup()
    picam2.stop()
    pygame.quit()
    quit()