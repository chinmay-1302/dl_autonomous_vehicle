import asyncio
import websockets
import cv2
import numpy as np
from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator
import json

SERVER_IP = "192.168.1.47"
SERVER_PORT = 8766
PAPER_CONF_THRESHOLD = 0.7
SIGNS_CONF_THRESHOLD = 0.5

# Load a pretrained YOLO model (recommended for training)
paper_model = YOLO('C:\Chinmay\Chinmay College Stuff\MIT-WPU\Sem 6\Mini Project\dl_av\models\paper\\best.pt')
paper_classes = ['paper - v1 2023-02-04 11-49pm']
# Get the model class names
print(paper_model.names)

# Load a pretrained YOLO model (recommended for training)
signs_model = YOLO('C:\Chinmay\Chinmay College Stuff\MIT-WPU\Sem 6\Mini Project\dl_av\models\left-right-road-signs-im\\best.pt')
# Get the model class names
print(signs_model.names)


async def receive_frames_and_send_predictions():
    async with websockets.connect(f"ws://{SERVER_IP}:{SERVER_PORT}") as websocket:
        while True:
            prediction = {}
            # Receive encoded frame from server
            encoded_frame = await websocket.recv()
            # Decode frame
            frame = cv2.imdecode(np.frombuffer(encoded_frame, dtype=np.uint8), cv2.IMREAD_COLOR)
            # Display the frame

            # Perform prediction using YOLO model
            paper_results = paper_model.predict(frame, conf=PAPER_CONF_THRESHOLD)
            paper_names_list = []
            for r in paper_results:
                annotator = Annotator(frame)
                boxes = r.boxes
                for box in boxes:
                    b = box.xyxy[0]  # get box coordinates in (left, top, right, bottom) format
                    c = box.cls
                    annotator.box_label(b, paper_model.names[int(c)])
                    if abs(int(b[3]) - int(b[1])) > 120:
                        paper_names_list.append(paper_model.names[int(c)])
                    # paper_names_list.append([int(b[0]),int(b[1]),int(b[2]),int(b[3])])
                    print(paper_model.names[int(c)])
                frame = annotator.result()

            signs_results = signs_model.predict(frame, conf=SIGNS_CONF_THRESHOLD)
            signs_names_list = []
            for r in signs_results:
                annotator = Annotator(frame)
                boxes = r.boxes
                for box in boxes:
                    b = box.xyxy[0]  # get box coordinates in (left, top, right, bottom) format
                    c = box.cls
                    annotator.box_label(b, signs_model.names[int(c)])
                    if abs(int(b[3]) - int(b[1])) > 120:
                        signs_names_list.append(signs_model.names[int(c)])
                    print(signs_model.names[int(c)])
                frame = annotator.result()
            cv2.imshow('Frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            # Process prediction results (for demonstration, just send the first prediction back to server)
            if paper_results:
                # prediction = str(names_list)
                prediction['paper_classes'] = paper_names_list
            else:
                # prediction = "No prediction"
                prediction['paper_classes'] = None

            if signs_results:
                prediction['signs_classes'] = signs_names_list
            else:
                prediction['signs_classes'] = None

            # Send prediction back to server
            await websocket.send(json.dumps(prediction))


# Run the client
asyncio.run(receive_frames_and_send_predictions())
