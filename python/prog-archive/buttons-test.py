import RPi.GPIO as GPIO
import time
import pygame
from pygame.locals import *

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

def debounce(button_pin):
    time.sleep(0.05)  # Adjust the sleep time based on your requirements
    return GPIO.input(button_pin)

try:
    while True:
        # TEST BUTTON
        if not debounce(21):
            print("test button is LOW (pressed), playing the next frame event as a test")
            LEDS_on()
            time.sleep(1)
            LEDS_off()

        # NEXT BUTTON
        if not debounce(17):
            print("next frame button is LOW (pressed)")
            LEDS_on()
            time.sleep(1)
            LEDS_off()

        # PREVIEW BUTTON
        if not debounce(22):
            print("preview button is LOW (pressed)")
            LEDS_on()
            time.sleep(1)
            LEDS_off()

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                print("q to quit")
                break

finally:
    # Release resources
    GPIO.cleanup()
    pygame.quit()
    quit()
