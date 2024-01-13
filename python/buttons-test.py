import RPi.GPIO as GPIO
import time
import keyboard  # Import the keyboard module

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # NEXT FRAME
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # PREVIEW
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # test button
GPIO.setup(18, GPIO.OUT)  # output (LED)  WHITE
GPIO.setup(24, GPIO.OUT)  # RED
GPIO.setup(27, GPIO.OUT)  # YELLOW
GPIO.setup(23, GPIO.OUT)  # GREEN
GPIO.setup(16, GPIO.OUT)  # IR

def stop_program():
    global stop_flag
    stop_flag = True
    pass

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
    
# Add an event listener for the 'Q' key to stop the program
keyboard.on_press_key('Q', stop_program)

try:
    while True:
                # TEST
        if not GPIO.input(21):
            print("test button is LOW (pressed), playing the next frame event as a test")
            LEDS_on()
            time.sleep(1)
            LEDS_off()

        # NEXT BUTTON
        if not GPIO.input(17):  # if port 17 == 0
            print("next frame button is LOW (pressed)")
            LEDS_on()
            time.sleep(1)
            LEDS_off()

        # PREVIEW
        if not GPIO.input(22):
            print("preview button is LOW (pressed)")
            LEDS_on()
            time.sleep(1)
            LEDS_off()



finally:
    # Release resourcesc
    GPIO.cleanup()
    keyboard.unhook_all()