import cv2
import asyncio
import websockets
import numpy as np

SERVER_IP = "ws://192.168.1.44:8766"

async def receive_video():
    async with websockets.connect(SERVER_IP) as websocket:
        while True:
            try:
                data = await websocket.recv()
                # Decode received data to image
                nparr = np.frombuffer(data, np.uint8)
                frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

                # Display the frame
                cv2.imshow('Video Stream', frame)

                # Check for user input to exit
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            except websockets.ConnectionClosed:
                print("Connection to server closed.")
                break

asyncio.run(receive_video())
