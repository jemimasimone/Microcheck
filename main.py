#for computer vision, allows access to cameras and usb devices
import cv2
# for handling errors?
import argparse

#yolo model
from ultralytics import YOLO
# for annotation, visualization (bounding boxes), filtering
import supervision as sv

# for camera resolution
def parse_arguments() -> argparse.Namespace:
    # print("Parser working")
    parser = argparse.ArgumentParser(description = "YOLOv8 live")
    parser.add_argument("--webcam-resolution",
                        default=[1280,720],
                        nargs=2,
                        type=int
    )
    args = parser.parse_args()
    return args

# main function
def main():
    # print("Hello! Main is working")

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

    while True:
        ret, frame = cap.read()

        # gets result from trained model
        result = model(frame)[0]

        # detections/annotations from model results
        detections = sv.Detections.from_ultralytics(result)

        # for detection dictionary
        print(f"Number of detections: {len(detections)}")  # Print the number of detections
        for detection in detections:
            print(detection)  # Print the content of each detection

        # get class labels, loop for each detection
        labels = []
        for (box, score, class_name, _), *_ in detections:
            # get class name
            class_name = detection[-1]['class_name']  # Access class_name from the last element of detection dictionary 
            # format label
            label_text = f"{class_name} - {score:0.2f}"  # Confidence rounded to 2 decimal places
            labels.append(label_text)  # Append the formatted label to the list

        # frame with bounding box
        annotated_frame = box_annotator.annotate(scene=frame, detections=detections)
        # frame with labels (final frame)
        frame = label_annotator.annotate(scene=annotated_frame, detections=detections, labels=labels)
        
        #display
        cv2.imshow("Microcheck", frame)

        # print(frame.shape)
        # break

        #closes program if ESC (ASCII 27) is pressed
        if (cv2.waitKey(30) == 27):
            break

# opens the file
if __name__ == "__main__":
    main()