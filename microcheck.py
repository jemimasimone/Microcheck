from pathlib import Path
from tkinter import Tk, Canvas, Button, PhotoImage
import cv2
import argparse
import numpy as np
from PIL import Image, ImageTk
from ultralytics import YOLO
import supervision as sv

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="YOLOv8 live")
    parser.add_argument("--canvas-width",
                        default=700,  # Default canvas width
                        type=int,
                        help="Width of the canvas for the camera feed")
    parser.add_argument("--canvas-height",
                        default=450,  # Default canvas height
                        type=int,
                        help="Height of the canvas for the camera feed")
    args = parser.parse_args()
    return args

args = parse_arguments()
canvas_width = args.canvas_width
canvas_height = args.canvas_height

# Initialize the webcam
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Unable to read camera feed")

# Optionally, you can set the camera resolution if needed
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, canvas_width)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, canvas_height)

model = YOLO("yolov8l.pt")
box_annotator = sv.BoundingBoxAnnotator(thickness=2)
label_annotator = sv.LabelAnnotator(text_thickness=2, text_scale=1)

# Define the zone polygon based on canvas size and center it
ZONE_POLYGON = np.array([
    [0, 0],
    [1.5, 0],
    [1.5, 2],
    [0, 2]
])

# Center the zone in the middle of the canvas
zone_width = canvas_width * 0.6  # Adjust the zone width as needed
zone_height = canvas_height * 0.6  # Adjust the zone height as needed

# Define the zone polygon centered in the canvas and ensure the coordinates are integers
zone_polygon = np.array([
    [(canvas_width - zone_width) / 2, (canvas_height - zone_height) / 2],
    [(canvas_width + zone_width) / 2, (canvas_height - zone_height) / 2],
    [(canvas_width + zone_width) / 2, (canvas_height + zone_height) / 2],
    [(canvas_width - zone_width) / 2, (canvas_height + zone_height) / 2]
], dtype=int)  # Ensure the coordinates are integers

zone = sv.PolygonZone(polygon=zone_polygon)
zone_annotator = sv.PolygonZoneAnnotator(
    zone=zone,
    color=sv.Color.WHITE,
    thickness=2,
    text_thickness=4,
    text_scale=2
)

window = Tk()
window.geometry(f"{canvas_width}x{canvas_height + 100}")  # Adjust window size based on canvas
window.configure(bg="#FFFFFF")
window.title("Microcheck")

# Create a canvas for the camera feed
camera_canvas = Canvas(window, width=canvas_width, height=canvas_height, bg="black")
camera_canvas.place(x=0, y=0)

# Create a canvas for the overlay (rectangle and buttons)
overlay_canvas = Canvas(window, width=canvas_width, height=100, bg="#FFFFFF", highlightthickness=0)
overlay_canvas.place(x=0, y=canvas_height)

# Draw the rectangle on the overlay canvas
overlay_canvas.create_rectangle(
    0.0,
    0.0,
    canvas_width,
    100,
    fill="#008CB8",
    outline=""
)

# Place buttons on the overlay canvas
button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_1 clicked"),
    relief="flat"
)
button_1.place(x=30.0, y=30.0, width=30.0, height=30.0)

button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_2 clicked"),
    relief="flat"
)
button_2.place(x=30.0, y=90.0, width=30.0, height=30.0)

button_image_3 = PhotoImage(file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    text="Fragment",
    compound="center",
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_3 clicked"),
    relief="flat",
    fg="#454545",
    font=("IstokWeb Bold", 15 * -1)
)
button_3.place(x=305.0, y=485.0, width=90.0, height=30.0)

button_image_4 = PhotoImage(file=relative_to_assets("button_4.png"))
button_4 = Button(
    image=button_image_4,
    text="Pellet",
    compound="center",
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_4 clicked"),
    relief="flat",
    fg="#454545",
    font=("IstokWeb Bold", 15 * -1)
)
button_4.place(x=55.0, y=485.0, width=90.0, height=30.0)

button_image_5 = PhotoImage(file=relative_to_assets("button_5.png"))
button_5 = Button(
    image=button_image_5,
    text="Fiber",
    compound="center",
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_5 clicked"),
    relief="flat",
    fg="#454545",
    font=("IstokWeb Bold", 15 * -1)
)
button_5.place(x=544.0, y=485.0, width=90.0, height=30.0)

button_image_all = PhotoImage(file=relative_to_assets("button_all.png"))
button_all = Button(
    image=button_image_all,
    text="All",
    compound="center",
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_all clicked"),
    relief="flat",
    fg="#454545",
    font=("IstokWeb Bold", 15 * -1)
)
button_all.place(x=305.0, y=30.0, width=90.0, height=30.0)

def update_frame():
    ret, frame = cap.read()
    
    if ret:
        # Resize the frame to fit the camera canvas
        frame_resized = cv2.resize(frame, (canvas_width, canvas_height))

        result = model(frame_resized, agnostic_nms=True)[0]
        detections = sv.Detections.from_ultralytics(result)
        detections = detections[detections.class_id != 0]

        labels = []
        for detection in detections:
            box, _, score, class_id, _, additional_info = detection
            class_name = additional_info['class_name']
            label_text = f"{class_name} - {score:0.2f}"
            labels.append(label_text)

        annotated_frame = box_annotator.annotate(scene=frame_resized, detections=detections)
        frame_with_labels = label_annotator.annotate(scene=annotated_frame, detections=detections, labels=labels)
        zone.trigger(detections=detections)
        frame_with_zones = zone_annotator.annotate(scene=frame_with_labels)

        frame_rgb = cv2.cvtColor(frame_with_zones, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame_rgb)
        imgtk = ImageTk.PhotoImage(image=img)
        
        camera_canvas.create_image(0, 0, anchor="nw", image=imgtk)
        camera_canvas.image = imgtk  # keep a reference
        
    window.after(10, update_frame)

window.after(10, update_frame)
window.mainloop()

cap.release()
cv2.destroyAllWindows()
