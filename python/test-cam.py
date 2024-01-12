from picamera2 import Picamera2
from libcamera import controls

focus = 0.5

picam2 = Picamera2()
picam2.start(show_preview=True)
picam2.set_controls({"AfMode": controls.AfModeEnum.Manual, "LensPosition": focus})