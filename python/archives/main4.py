import pygame
import os

# Initialize Pygame
pygame.init()

# Set the current working directory to the script's location
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# Set display size
screen_size = (640, 480)  # Example size, adjust as necessary
screen = pygame.display.set_mode(screen_size)

# Load the image
image_path = 'preview_frame.jpg'
if os.path.exists(image_path):
    try:
        image = pygame.image.load(image_path)
        image = pygame.transform.scale(image, screen_size)
        screen.blit(image, (0, 0))
        pygame.display.flip()
    except Exception as e:
        print(f"Failed to load image: {e}")
else:
    print(f"Image does not exist at path: {image_path}")

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()