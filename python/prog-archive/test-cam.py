import RPi.GPIO as GPIO
import cv2
from picamera2 import Picamera2
import time
picam2 = Picamera2()
picam2.preview_configuration.main.size = (1280,720)
picam2.preview_configuration.main.format = "RGB888"
picam2.preview_configuration.align()
picam2.configure("preview")
picam2.start()
picam2.sensor_resolution
while True:
    im= picam2.capture_array()
    cv2.imshow("Camera", im)
    if cv2.waitKey(1)==ord('q'):
        break
cv2.destroyAllWindows()

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # NEXT FRAME
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # PREVIEW
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # test button
GPIO.setup(18, GPIO.OUT)  # output (LED)  WHITE
GPIO.setup(24, GPIO.OUT)  # RED
GPIO.setup(27, GPIO.OUT)  # YELLOW
GPIO.setup(23, GPIO.OUT)  # GREEN
GPIO.setup(16, GPIO.OUT)  # IR

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


try:
    while True:
        LEDS_on()


        # TEST
        if not GPIO.input(21):
            print("test button is LOW (pressed), playing the next frame event as a test")
            LEDS_off()
            time.sleep(1)




        # NEXT BUTTON
        if not GPIO.input(17): 
            print("next frame button is LOW (pressed)")
            LEDS_off()
            time.sleep(1)


        # PREVIEW
        if not GPIO.input(22):
            print("preview button is LOW (pressed)")
            LEDS_off()
            time.sleep(1)

finally:
    # Release resources
    time.quit()
    picam2.stop_preview()