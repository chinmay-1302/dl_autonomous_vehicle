import asyncio
import websockets
import numpy as np
import cv2
import json


# RASPBERRY_PI_IP = "192.168.1.25"
# RASPBERRY_PI_IP = "10.23.16.71"
RASPBERRY_PI_IP = "192.168.1.46"
GESTURE_PORT = 8765
STREAM_PORT = 8766
VIDEO_SOURCE = 0
VIDEO_WIDTH = 640
VIDEO_HEIGHT = 480

async def echo(websocket, path):
    async for message in websocket:
        print("Received message:", message)
        await websocket.send(message)


async def video_stream(websocket, path):
    print("Video stream started")
    cap = cv2.VideoCapture(VIDEO_SOURCE)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, VIDEO_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, VIDEO_HEIGHT)
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
    video_server = websockets.serve(video_stream, RASPBERRY_PI_IP, STREAM_PORT)  # Run video server on port 8766

    await asyncio.gather(echo_server, video_server)


asyncio.get_event_loop().run_until_complete(main())
asyncio.get_event_loop().run_forever()
