import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import cv2
import matplotlib.pyplot as plt
import math
from PIL import Image
import numpy as np

DESIRED_HEIGHT = 480
DESIRED_WIDTH = 480
VIDEO_SOURCE = 2


def resize_and_show(image):
    h, w = image.shape[:2]
    if h < w:
        img = cv2.resize(image, (DESIRED_WIDTH, math.floor(h/(w/DESIRED_WIDTH))))
    else:
        img = cv2.resize(image, (math.floor(w/(h/DESIRED_HEIGHT)), DESIRED_HEIGHT))
    cv2.imshow(img)


base_options = python.BaseOptions(model_asset_path='C:\Chinmay\Chinmay College Stuff\MIT-WPU\Sem 6\Mini Project\dl_av\manas\gesture_recognizer.task')
options = vision.GestureRecognizerOptions(base_options=base_options)
recognizer = vision.GestureRecognizer.create_from_options(options)


cap = cv2.VideoCapture(VIDEO_SOURCE)
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)

    # STEP 4: Recognize gestures in the input image.
    recognition_result = recognizer.recognize(image)

    # STEP 5: Process the result. In this case, visualize it.
    cv2.imshow('frame', frame)
    # top_gesture = recognition_result.gestures[0][0]
    top_gesture = recognition_result.gestures
    hand_landmarks = recognition_result.hand_landmarks
    print(hand_landmarks)

cap.release()
cv2.waitKey(0)
cv2.destroyAllWindows()
