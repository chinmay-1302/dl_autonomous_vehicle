import asyncio
import websockets
import cv2
import numpy as np
from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator
from PIL import Image


# RASPBERRY_PI_IP = "192.168.1.25"
RASPBERRY_PI_IP = "192.168.1.44"
PORT = 8766
VIDEO_SOURCE = 2

# Load a pretrained YOLO model (recommended for training)
# model = YOLO('C:\Chinmay\Chinmay College Stuff\MIT-WPU\Sem 6\Mini Project\dl_av\models\paper\\best.pt')
model = YOLO('C:\Chinmay\Chinmay College Stuff\MIT-WPU\Sem 6\Mini Project\dl_av\models\left-right-road-signs-im\\best.pt')
#classes = ['paper - v1 2023-02-04 11-49pm']
classes = ['paper - v1 2023-02-04 11-49pm']
conf_thres = 0.5

# Get the model class names
print(model.names)


async def video_stream(websocket, path):
    cap = cv2.VideoCapture(VIDEO_SOURCE)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        results = model.predict(frame, conf=conf_thres)
        for r in results:
            annotator = Annotator(frame)
            boxes = r.boxes
            for box in boxes:
                b = box.xyxy[0]  # get box coordinates in (left, top, right, bottom) format
                c = box.cls
                annotator.box_label(b, model.names[int(c)])
                print(model.names[int(c)])
            frame = annotator.result()
            # frame = cv2.cvtColor(np.array(frame), cv2.COLOR_BGR2RGB)
            #frame = cv2.cvtColor(np.array(frame), cv2.COLOR_BGR2RGB)
        # Encode frame as JPEG
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
        _, encoded_frame = cv2.imencode('.jpg', frame, encode_param)
        data = np.array(encoded_frame).tobytes()

        try:
            await websocket.send(data)
        except websockets.ConnectionClosed:
            break

    cap.release()

async def server():
    async with websockets.serve(video_stream, RASPBERRY_PI_IP, PORT):
        print(f"Server started at ws://{RASPBERRY_PI_IP}:{PORT}")
        await asyncio.Future()  # Run forever

asyncio.run(server())