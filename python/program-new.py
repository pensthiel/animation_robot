#!/usr/bin/python3

# Import necessary libraries
import typing
import numpy
import cv2
from picamera2 import Picamera2, Preview
import RPi.GPIO as GPIO
import os
import time
import pygame
from pygame.locals import *

# pic size 1536 x 864
# screen size 1920 x 1080, 16:9
#[(160, -80), (1760, -80), (1760, 1160), (160, 1160)] rectangle

# top left
TLw = -150
TLh = 0
# top right
TRw = 1600
TRh = 0
# bottom right
BRw = 1600
BRh = 1200
# bottom left
BLw = -150
BLh = 1200

#camera controls
zoom = 1 # horizontal
zoomVertical = 1 # vertical
offset_tweak_left = 0  
offset_tweak_top = 0  

#image display controls
moveRight = 0
moveDown = 0
imgWidthOffset = 0
imgHeightOffset = 0

exp = 2000
gain = 3
focus = 1
red = 0
blue = 0

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # NEXT FRAME
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # quit button


pygame.mixer.pre_init()
# Initialize Pygame
pygame.init()
screen_size = (0, 0)  # Set to (0, 0) for full screen
screen = pygame.display.set_mode(screen_size, pygame.FULLSCREEN) # Set display size
screen_info = pygame.display.Info() # Get the current display info
width = screen_info.current_w
height = screen_info.current_h
pygame.mouse.set_visible(False)

# Create a Picamera2 instance
picam2 = Picamera2()
print("picam init")
print(f"{screen_size}")
print(f"{width}, {height}")

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
print("bell sound file path:", os.path.abspath("samples/bell.mp3"))
print("music sound file path:", os.path.abspath("samples/music.mp3"))



y_key_pressed = False

frame_to_display = None
next_button_pressed = False
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
sizeWidth = int(size[0] * zoom)
sizeHeight = int(size[1] * zoomVertical)
#offset = [(r - s) // 2 for r, s in zip(full_res, size)]
#picam2.set_controls({"ScalerCrop": offset + size})

# Calculate offset based on the initial values
offset_width = (full_res[0] - sizeWidth) // 2 + offset_tweak_left
offset_height = (full_res[1] - sizeHeight) // 2 + offset_tweak_top

# Create a list with the individual offset values
offset = [offset_width, offset_height]
size = [sizeWidth, sizeHeight]
print(f"offset : {offset}")
metadata = picam2.capture_metadata()
controls = {c: metadata[c] for c in ["ExposureTime", "AnalogueGain", "ColourGains","ColourTemperature","LensPosition"]}
print(controls)
# Set controls with individual offset values
picam2.set_controls({"AwbEnable": 0})
picam2.set_controls({"ScalerCrop": offset + size,"ExposureTime": exp, "AnalogueGain": gain,"AfMode": 0, "LensPosition": focus,"ColourGains": (red, blue)})



def warp(surf: pygame.Surface, warp_pts, smooth=True, out: pygame.Surface = None) -> typing.Tuple[pygame.Surface, pygame.Rect]:
    """Stretches a pygame surface to fill a quad using cv2's perspective warp.

        Args:
            surf: The surface to transform.
            warp_pts: A list of four xy coordinates representing the polygon to fill.
                Points should be specified in clockwise order starting from the top left.
            smooth: Whether to use linear interpolation for the image transformation.
                If false, nearest neighbor will be used.
            out: An optional surface to use for the final output. If None or not
                the correct size, a new surface will be made instead.

        Returns:
            [0]: A Surface containing the warped image.
            [1]: A Rect describing where to blit the output surface to make its coordinates
                match the input coordinates.
    """
    if len(warp_pts) != 4:
        raise ValueError("warp_pts must contain four points")

    w, h = surf.get_size()
    is_alpha = surf.get_flags() & pygame.SRCALPHA

    # XXX throughout this method we need to swap x and y coordinates
    # when we pass stuff between pygame and cv2. I'm not sure why .-.
    src_corners = numpy.float32([(0, 0), (0, w), (h, w), (h, 0)])
    quad = [tuple(reversed(p)) for p in warp_pts]

    # find the bounding box of warp points
    # (this gives the size and position of the final output surface).
    min_x, max_x = float('inf'), -float('inf')
    min_y, max_y = float('inf'), -float('inf')
    for p in quad:
        min_x, max_x = min(min_x, p[0]), max(max_x, p[0])
        min_y, max_y = min(min_y, p[1]), max(max_y, p[1])
    warp_bounding_box = pygame.Rect(int(min_x), int(min_y),
                                    int(max_x - min_x),
                                    int(max_y - min_y))

    shifted_quad = [(p[0] - min_x, p[1] - min_y) for p in quad]
    dst_corners = numpy.float32(shifted_quad)

    mat = cv2.getPerspectiveTransform(src_corners, dst_corners)

    orig_rgb = pygame.surfarray.pixels3d(surf)

    flags = cv2.INTER_LINEAR if smooth else cv2.INTER_NEAREST
    out_rgb = cv2.warpPerspective(orig_rgb, mat, warp_bounding_box.size, flags=flags)

    if out is None or out.get_size() != out_rgb.shape[0:2]:
        out = pygame.Surface(out_rgb.shape[0:2], pygame.SRCALPHA if is_alpha else 0)

    pygame.surfarray.blit_array(out, out_rgb)

    if is_alpha:
        orig_alpha = pygame.surfarray.pixels_alpha(surf)
        out_alpha = cv2.warpPerspective(orig_alpha, mat, warp_bounding_box.size, flags=flags)
        alpha_px = pygame.surfarray.pixels_alpha(out)
        alpha_px[:] = out_alpha
    else:
        out.set_colorkey(surf.get_colorkey())

    # XXX swap x and y once again...
    return out, pygame.Rect(warp_bounding_box.y, warp_bounding_box.x,
                            warp_bounding_box.h, warp_bounding_box.w)




def save_frame(prefix='frame', file_format='jpg'):
    try:
        global frame_number,frame_to_display  # Declare both as global
        filename = f"{prefix}_{frame_number}.{file_format}"
        print(filename)
        filepath = os.path.join("reload", filename)
        print(filepath)

        # Fill the screen with a black background
        screen.fill((0,0,0))
        try:
            os.system(" sudo uhubctl -l 1-1 -a 1")
        except Exception as e:
            print("Error playing sound:", e)
        pygame.display.flip()  # Update the display
        time.sleep(0.3)
        picam2.capture_metadata()
        picam2.capture_file(filepath)
        frame_to_display = filepath
        frame_number += 1
        time.sleep(0.2)
        try:
            os.system(" sudo uhubctl -l 1-1 -a 0")
        except Exception as e:
            print("Error playing sound:", e)




    except Exception as error:
        print(f"Failed to take and save frame: {error}")



def debounce(button_pin):
    time.sleep(0.05)  # Adjust the sleep time based on your requirements
    return GPIO.input(button_pin)



screen.fill((200, 150, 250))
pygame.mixer.Sound.play(music)
try:
    os.system(" sudo uhubctl -l 1-1 -a 0")
except Exception as e:
    print("Error playing sound:", e)

try:
    while True:
        pygame.display.flip()



        if not debounce(17):
            print("next button pressed")
            next_button_pressed = True

        if not debounce(21):
            print("exit button pressed")
            break


        if next_button_pressed:
            pygame.mixer.Sound.stop(music)
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
                        scaled_image = pygame.transform.scale(image, ((width + imgWidthOffset), (height + imgHeightOffset)))
                        
                        #added code. see if it works-----------------------------
                        
                        default_rect = scaled_image.get_rect(center=screen.get_rect().center)
                        warped_img = None
                        
                        corners = [list(default_rect.topleft), list(default_rect.topright), 
                                   list(default_rect.bottomright), list(default_rect.bottomleft)]
                        
                        print(corners)
                        
                        # Corner 1
                        corners[0][0] = TLw
                        corners[0][1] = TLh

                        # Corner 2
                        corners[1][0] = TRw
                        corners[1][1] = TRh

                        # Corner 3
                        corners[2][0] = BRw
                        corners[2][1] = BRh

                        # Corner 4
                        corners[3][0] = BLw
                        corners[3][1] = BLh
                        
                        print(corners)
                        
                        pts_to_use = corners #you can manually change the values of the corners for now. example had fancy click and drag stuff.
                        
                        warped_img, warped_pos = warp(
                            scaled_image,
                            pts_to_use,
                            smooth=True,  # dont really know what this does. keeping it on true
                            out=warped_img)
                        
                        #end-----------------------------------------------------
                        
                        screen.blit(warped_img, warped_pos)
                        
                        pygame.display.flip()
                        print("frame displayed")


                    except Exception as load_error:
                        print(f"Failed to load image: {load_error}")

            except Exception as file_error:
                print("Error occurred while loading image.")  # Use error handling to catch and report any issues smoothly.

            next_button_pressed = False
            print("next_button_pressed = False")
            y_key_pressed = False



        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):

                print("q to quit")
                exit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_y:
                print("y key event detected")
                if not y_key_pressed:
                    print("next frame triggered with y key")
                    next_button_pressed = True
                    y_key_pressed = True  # Set the variable to True after the action



except Exception as file_error:
    print(f"error initinalising loop: {file_error}")





except KeyboardInterrupt:
    pass  # Handle the Ctrl+C interrupt to gracefully exit the program


finally:
    # Release resources
    pygame.mixer.quit()
    GPIO.cleanup()
    picam2.stop()
    pygame.quit()
    quit()