#for computer vision, allows access to cameras and usb devices
import cv2
# for handling errors?
import argparse

#yolo model
from ultralytics import YOLO
# for annotation, visualization (bounding boxes), filtering
import supervision as sv
# for arrays and pixel location in defining polygon zones
import numpy as np

# Define a polygon zone in the frame
ZONE_POLYGON = np.array([
    # [x-axis, y-axis]
    [0,0], # Top-left corner of the rectangle
    [1.5,0],  # Top-right corner of the rectangle
    [1.5,2], # Bottom-right corner of the rectangle
    [0,2] # Bottom-left corner of the rectangle
])

# for camera resolution
def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description = "YOLOv8 live")
    parser.add_argument("--webcam-resolution",
                        default=[1280,720], # [width, height]
                        nargs=2,
                        type=int
    )
    args = parser.parse_args()
    return args

# main function
def main():
    # calls def for camera resolution, sets value to 
    args = parse_arguments()
    frame_width, frame_height = args.webcam_resolution

    # accesses the default camera (index 0)
    cap = cv2.VideoCapture(0)
    # sets the frame width and height
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)

    # call model
    model = YOLO("yolov8l.pt")

    # bounding box feature
    box_annotator = sv.BoundingBoxAnnotator(thickness=2)
    #label feature
    label_annotator = sv.LabelAnnotator(text_thickness=2, text_scale=1)

    # Define the polygon zone and annotator
    zone_polygon = (ZONE_POLYGON * np.array(args.webcam_resolution)).astype(int)
    zone = sv.PolygonZone(polygon=zone_polygon)
    zone_annotator = sv.PolygonZoneAnnotator(
        zone=zone,
        color=sv.Color.WHITE,
        thickness=2,
        text_thickness=4,
        text_scale=2
        )

    while True:
        ret, frame = cap.read()

        # gets result from trained model
        result = model(frame, agnostic_nms=True)[0]

        # detections/annotations from model results
        detections = sv.Detections.from_ultralytics(result)

        # filter detection
        detections = detections[detections.class_id != 0] # model doesn't detect people (class_id = 0)

        # for detection dictionary
        print(f"Number of detections: {len(detections)}")  # Print the number of detections
        for detection in detections:
            print(detection)  # Print the content of each detection

        # get class labels, loop for each detection
        labels = []
        for detection in detections:
            box, _, score, class_id, _, additional_info = detection
            class_name = additional_info['class_name']  # Access class_name from additional_info dictionary 
            # format label
            label_text = f"{class_name} - {score:0.2f}"  # Confidence rounded to 2 decimal places
            labels.append(label_text)  # Append the formatted label to the list

        # frame with bounding box
        annotated_frame = box_annotator.annotate(scene=frame, detections=detections)
        # frame with labels (final frame)
        frame = label_annotator.annotate(scene=annotated_frame, detections=detections, labels=labels)
        
        # annotate frame with zones
        zone.trigger(detections=detections)
        frame = zone_annotator.annotate(scene=frame)

        #display
        cv2.imshow("Microcheck", frame)

        #closes program if ESC (ASCII 27) is pressed
        if (cv2.waitKey(30) == 27):
            break

# opens the file
if __name__ == "__main__":
    main()