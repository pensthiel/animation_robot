#!/usr/bin/python3

# Import necessary libraries


import os
import time
import pygame
from pygame.locals import *


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

for root_dir, cur_dir, files in os.walk(reload_folder):
    frame_number += len(files)
    frame_number -= 1

print('File count in', reload_folder, ':', frame_number)


frame_to_display = None

filepath = None
filepath2 = None

# Frame count initializations

preview_number = 0


screen.fill((200, 150, 250))

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


try:
    while True:
        


        print("preview starts")
        filepath2 = os.path.join("reload", f"frame_{preview_number}.jpg")
        preview_number += 1
        print(filepath2)
        if os.path.exists(filepath2):  # Checking for file existence outside the loop can speed up significantly
            try:
                
                image = pygame.image.load(filepath2)
                print(filepath2 + " loaded")
                scaled_image = pygame.transform.scale(image, (width, height))
                print(filepath2 + "scaled")
                screen.blit(scaled_image, (0, 0))
                pygame.display.flip()
                print(filepath2 + " displayed")
                time.sleep(delay)

            except Exception as file_error:
               print(f"Error occurred while loading the image. {file_error}")   # Use error handling to catch and report any issues smoothly.

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