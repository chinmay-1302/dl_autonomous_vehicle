import asyncio
import websockets
import cv2
import numpy as np
from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator

SERVER_IP = "192.168.1.44"
SERVER_PORT = 8767
CONF_THRESHOLD = 0.7

# Load a pretrained YOLO model (recommended for training)
model = YOLO('C:\Chinmay\Chinmay College Stuff\MIT-WPU\Sem 6\Mini Project\dl_av\models\paper\\best.pt')
classes = ['paper - v1 2023-02-04 11-49pm']
# classes = ['paper - v1 2023-02-04 11-49pm']
conf_thres = 0.5

# Get the model class names
print(model.names)


async def receive_frames_and_send_predictions():
    async with websockets.connect(f"ws://{SERVER_IP}:{SERVER_PORT}") as websocket:
        while True:
            # Receive encoded frame from server
            encoded_frame = await websocket.recv()
            # Decode frame
            frame = cv2.imdecode(np.frombuffer(encoded_frame, dtype=np.uint8), cv2.IMREAD_COLOR)
            # Display the frame
            # Perform prediction using YOLO model
            results = model.predict(frame, conf=CONF_THRESHOLD)
            names_list = []
            for r in results:
                annotator = Annotator(frame)
                boxes = r.boxes
                for box in boxes:
                    b = box.xyxy[0]  # get box coordinates in (left, top, right, bottom) format
                    c = box.cls
                    annotator.box_label(b, model.names[int(c)])
                    names_list.append(model.names[int(c)])
                    print(model.names[int(c)])
                frame = annotator.result()
            cv2.imshow('Frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            # Process prediction results (for demonstration, just send the first prediction back to server)
            if results:
                prediction = str(names_list)
            else:
                prediction = "No prediction"
            # Send prediction back to server
            await websocket.send(prediction)


# Run the client
asyncio.run(receive_frames_and_send_predictions())
