import cv2

# Set up the window
cv2.namedWindow("Webcam Feed", cv2.WINDOW_FULLSCREEN)
cv2.setWindowProperty("Webcam Feed", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

def quit_program():
    cv2.destroyAllWindows()
    exit()

# Replace 0 with the appropriate camera index (e.g., 0 for the built-in camera)
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    if not ret:
        break

    cv2.imshow("Webcam Feed", frame)

    key = cv2.waitKey(1)
    if key == ord('q'):
        quit_program()

cap.release()
