import cv2
import mediapipe as mp

# Define aliases for easier access to classes
BaseOptions = mp.tasks.BaseOptions
GestureRecognizer = mp.tasks.vision.GestureRecognizer
GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
GestureRecognizerResult = mp.tasks.vision.GestureRecognizerResult
VisionRunningMode = mp.tasks.vision.RunningMode

# Callback function to handle gesture recognition results
def print_result(result: GestureRecognizerResult, output_image: mp.Image, timestamp_ms: int):
    print('Gesture recognition result:', result)

# Open a video capture device (e.g., webcam)
cap = cv2.VideoCapture(2)  # Use 0 for the default webcam

# Check if the capture device is opened successfully
if not cap.isOpened():
    print("Error: Couldn't open video capture device")
    exit()

# Define options for the gesture recognizer
options = GestureRecognizerOptions(
    base_options=BaseOptions(model_asset_path='gesture_recognizer.task'),
    running_mode=VisionRunningMode.LIVE_STREAM,
    result_callback=print_result
)

# Create a gesture recognizer instance
with GestureRecognizer.create_from_options(options) as recognizer:

    # Loop to continuously capture and process frames
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Check if the frame is captured successfully
        if not ret:
            print("Error: Couldn't capture frame")
            break

        # Process the frame with the gesture recognizer
        results = recognizer.process(frame)

        # Display the captured frame
        cv2.imshow('Frame', frame)

        # Check for the 'q' key to exit the loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Release the capture device and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
