#!/usr/bin/python3

# Import necessary libraries


import os
import time
import pygame
from pygame.locals import *

film_lenght = 25 # Number of frames to play 5 fps, 75 frames = 15 seconds

folder_name="reload" # Folder name to load images from

delay = 0.2 # 0.2 is 20% of a second I think ? = 5fps i guess


pygame.mixer.pre_init()
# Initialize Pygame
pygame.init()
screen_size = (0, 0)  # Set to (0, 0) for full screen
screen = pygame.display.set_mode(screen_size, pygame.FULLSCREEN) # Set display size
screen_info = pygame.display.Info() # Get the current display info
width = screen_info.current_w
height = screen_info.current_h


# Set the current working directory to the script's location
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# NUMBER OF FILES IN THE "RELOAD" FOLDER
reload_folder = os.path.join(script_dir, folder_name)
frame_number = 0

exagon = pygame.image.load(os.path.join("samples", "exagon.png"))

# Calculate the scale factor to fit the exagon to the screen width while maintaining aspect ratio
scale_factor = height / exagon.get_height()
print(scale_factor)

# Scale the exagon image
scaled_exa = pygame.transform.rotozoom(exagon, 0, scale_factor)

# Calculate the margin to center the scaled exagon horizontally on the screen
margin2 = (width - scaled_exa.get_width()) // 2




print('File count in', reload_folder, ':', frame_number)


frame_to_display = None

filepath = None
filepath2 = None

# Frame count initializations

preview_number = 0



screen.fill((0,0,0))
pygame.mouse.set_visible(False)
pygame.display.flip()


try:
    while True:
        

        for root_dir, cur_dir, files in os.walk(reload_folder):
            frame_number = len(files)
            frame_number -= 1
            print('File count in', reload_folder, ':', frame_number)

        print("preview starts")
        filepath2 = os.path.join("reload", f"frame_{preview_number}.jpg")
        preview_number += 1
        print(filepath2)
        if os.path.exists(filepath2):  # Checking for file existence outside the loop can speed up significantly
            try:
                
                image = pygame.image.load(filepath2)
                print(filepath2 + " loaded")
                # Calculate the scale factor to fit the image to the screen height while maintaining aspect ratio
                scale_factor = height / image.get_height()
                
                # Scale the image
                scaled_image = pygame.transform.rotozoom(image, 0, scale_factor)
                
                # Calculate the margin to center the scaled image horizontally on the screen
                imgwidth, imgheight = scaled_image.get_size()
                margin = (width - imgwidth) // 2
                
                # Blit the scaled image and the scaled exagon onto the screen
                screen.blit(scaled_image, (margin, 0))
                screen.blit(scaled_exa, (margin2, 0))
                pygame.display.flip()
                print(filepath2 + " displayed")
                time.sleep(delay)

            except Exception as file_error:
               print(f"Error occurred while loading the image. {file_error}")   # Use error handling to catch and report any issues smoothly.

        else:
            print("can't preview: Directory empty")

        try:
            if preview_number == frame_number:
                if frame_number > (film_lenght+1):
                    preview_number = frame_number -film_lenght
                else:
                    preview_number = 0

            pygame.mixer.stop()
        except Exception as e:
            print(f"error stopping preview: {e}")


        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):

                print("q to quit")
                exit()

            



except KeyboardInterrupt:
    pass  # Handle the Ctrl+C interrupt to gracefully exit the program


finally:
    # Release resources
    pygame.quit()
    quit()