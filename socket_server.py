import asyncio
import websockets
from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator
import numpy as np
import cv2
import threading
import json


# RASPBERRY_PI_IP = "192.168.1.25"
# RASPBERRY_PI_IP = "10.23.16.71"
RASPBERRY_PI_IP = "192.168.1.46"
GESTURE_PORT = 8765
SIGN_STREAM_PORT = 8766
PAPER_STREAM_PORT = 8767
VIDEO_SOURCE = 0


async def echo(websocket, path):
    async for message in websocket:
        print("Received message:", message)
        await websocket.send(message)


async def sign_video_stream(websocket, path):
    print("Video stream started")
    cap = cv2.VideoCapture(VIDEO_SOURCE)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        # Encode frame as JPEG
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
        _, encoded_frame = cv2.imencode('.jpg', frame, encode_param)
        data = np.array(encoded_frame).tobytes()
        try:
            await websocket.send(data)
            prediction = await websocket.recv()
            if len(prediction) > 2:
                prediction = prediction[1:-1]
                print("Received prediction:", prediction)
        except websockets.ConnectionClosed:
            break
    cap.release()


async def paper_video_stream(websocket, path):
    print("Video stream started")
    cap = cv2.VideoCapture(VIDEO_SOURCE)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        # Encode frame as JPEG
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
        _, encoded_frame = cv2.imencode('.jpg', frame, encode_param)
        data = np.array(encoded_frame).tobytes()
        try:
            await websocket.send(data)
            prediction = await websocket.recv()
            prediction_dict = json.loads(prediction)
            print(prediction_dict)
            await asyncio.sleep(1)
        except websockets.ConnectionClosed:
            break
    cap.release()


async def main():
    echo_server = websockets.serve(echo, RASPBERRY_PI_IP, GESTURE_PORT)  # Run echo server on port 8765
    sign_video_server = websockets.serve(sign_video_stream, RASPBERRY_PI_IP, SIGN_STREAM_PORT)  # Run video server on port 8766
    paper_video_server = websockets.serve(paper_video_stream, RASPBERRY_PI_IP, PAPER_STREAM_PORT)  # Run video server on port 8767

    await asyncio.gather(echo_server, sign_video_server, paper_video_server)


asyncio.get_event_loop().run_until_complete(main())
asyncio.get_event_loop().run_forever()
