# import a utility function for loading Roboflow models
from inference import get_model
# import supervision to visualize our results
import supervision as sv
# import cv2 to helo load our image
import cv2
import os

# define the image url to use for inference
image_file = "images/paper_lane/1.jpg"
image = cv2.imread(image_file)

# load a pre-trained yolov8n model
# model = get_model(model_id="paper-8afbw/1")
model = get_model(model_id="tyukin_detection_books/2")

directory = 'images/paper_lane'
output_directory = 'images/paper_lane_detected'
for image_path in os.listdir(directory):
    # create the full input path and read the file
    input_path = os.path.join(directory, image_path)
    image_to_pred = cv2.imread(input_path)
    cv2.imshow(image_path, image_to_pred)

    # run inference on our chosen image, image can be a url, a numpy array, a PIL image, etc.
    results = model.infer(image_to_pred)

    # load the results into the supervision Detections api
    detections = sv.Detections.from_inference(results[0].dict(by_alias=True, exclude_none=True))

    # create supervision annotators
    bounding_box_annotator = sv.BoundingBoxAnnotator()
    label_annotator = sv.LabelAnnotator()

    # annotate the image with our inference results
    annotated_image = bounding_box_annotator.annotate(
       scene=image_to_pred, detections=detections)
    annotated_image = label_annotator.annotate(
       scene=annotated_image, detections=detections)

    fullpath = os.path.join(output_directory, 'pred_' + image_path)
    cv2.imwrite(fullpath, annotated_image)
    cv2.waitKey(0)  # waits until a key is pressed

# display the image
#sv.plot_image(annotated_image)