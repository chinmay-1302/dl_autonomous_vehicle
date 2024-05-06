from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator
from PIL import Image
import cv2

# Load a pretrained YOLO model (recommended for training)
# model = YOLO('models/paper/best.pt')
model = YOLO('models/left-right-road-signs-im/best.pt')

# Get the model class names
print(model.names)
names = model.names

# Perform object detection on an image using the model
# img = cv2.imread('images/paper-ball-wars.jpg')
img = cv2.imread('images/right-road-sign-2.png')
#img = cv2.imread('images/left-road-sign-2.png')
results = model.predict(img)
print(results)
for r in results:
    annotator = Annotator(img)
    boxes = r.boxes
    for box in boxes:
        b = box.xyxy[0]  # get box coordinates in (left, top, right, bottom) format
        c = box.cls
        annotator.box_label(b, model.names[int(c)])
        print("Class: ", model.names[int(c)])
    img = annotator.result()
    img = Image.fromarray(img)
    img.show()