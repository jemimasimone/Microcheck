import sys
import cv2
import os
import numpy as np
from PIL import Image, ImageTk
from pathlib import Path
from tkinter import Tk, Canvas, Button, PhotoImage, filedialog
import tkinter.font as tkFont
from ultralytics import YOLO
import supervision as sv
import datetime

# GUI ----------------

if getattr(sys, 'frozen', False):
    BASE_PATH = sys._MEIPASS
else:
    BASE_PATH = os.path.dirname(os.path.abspath(__file__))

def relative_to_assets(path: str) -> Path:
    return Path(BASE_PATH) / 'assets' / path

model_path = Path(BASE_PATH) / 'yolo_microplastic.pt'

def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")

def update_canvas(*args):
    canvas.config(width=window.winfo_width(), height=window.winfo_height())

    footer_height = int(window.winfo_height() * 0.15)  
    footer_y = window.winfo_height() - footer_height
    canvas.coords(footer_rect, 0, footer_y, window.winfo_width(), window.winfo_height())

    button_width = int(window.winfo_width() * 0.13) 
    button_height = int(footer_height * 0.6)  
    spacing = (window.winfo_width() - button_width * 2) // 3

    font_size = int(window.winfo_width() * 0.015) 
    button_font = tkFont.Font(family="IstokWeb Bold", size=font_size)
    for button in [button_3, button_4, button_5]:
        button.config(font=button_font)

    button_positions = {
        button_3: (window.winfo_width() // 2 - button_width // 2, footer_y + (footer_height - button_height) // 2),
        button_4: (spacing, footer_y + (footer_height - button_height) // 2),
        button_5: (window.winfo_width() - button_width - spacing, footer_y + (footer_height - button_height) // 2)
    }

    for button, (x, y) in button_positions.items():
        button.place(x=x, y=y, width=button_width, height=button_height)
    
    update_zone_polygon()

def update_zone_polygon():
    global zone_polygon
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()

    zone_polygon = np.array([
        [0, 0],
        [canvas_width, 0],
        [canvas_width, canvas_height],
        [0, canvas_height]
    ], dtype=int)

def adjust_label_position(label_x, label_y, frame_width, frame_height):
    margin = 10
    if label_y < margin:
        label_y = margin
    if label_y > frame_height - margin:
        label_y = frame_height - margin
    return label_x, label_y

window = Tk()
window_width = 700
window_height  = 550

center_window(window, window_width, window_height)
window.configure(bg="#008CB8")
window.title("Microcheck")

window.minsize(window_width, window_height)

canvas = Canvas(
    window,
    bg="#FFFFFF",
    relief="flat"
)

canvas.grid(row=0, column=0, sticky="nsew")

footer_height = 100
footer_rect = canvas.create_rectangle(
    0, window_height - footer_height,
    window_width, window_height,
    outline=""
)

button_image_3 = PhotoImage(file=relative_to_assets("button_3.png"))
button_image_4 = PhotoImage(file=relative_to_assets("button_4.png"))
button_image_5 = PhotoImage(file=relative_to_assets("button_5.png"))

update_zone_polygon()
zone = sv.PolygonZone(polygon=zone_polygon)
zone_annotator = sv.PolygonZoneAnnotator(
    zone=zone,
    color=sv.Color.BLUE,
    text_scale=0,
    text_thickness=0,
    thickness=0
)

box_annotator = sv.BoundingBoxAnnotator(thickness=2)
label_annotator = sv.LabelAnnotator(text_thickness=1, text_scale=0.5)

# MODEL ---------
is_running = False
model = None
current_frame = None

def detect():
    global is_running, model
    is_running = True
    if model is None:
        model = YOLO(model_path)

def stop():
    global is_running, model
    is_running = False
    model = None

def save_frame():
    global current_frame
    if current_frame is not None:
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            filename = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".png"
            filepath = Path(folder_selected) / filename
            cv2.imwrite(str(filepath), cv2.cvtColor(current_frame, cv2.COLOR_RGB2BGR))
            print(f"Image saved as {filepath}")

# Buttons
button_3 = Button(
    text="Capture",
    compound="center",
    command=save_frame,
    relief="raised",
    fg="#454545",
    font=("IstokWeb Bold", 15 * -1),
    cursor="hand2",
    padx=10,
    pady=10,
    activebackground="light gray",
    activeforeground="black"
)

button_4 = Button(
    text="Start",
    compound="center",
    command=detect,
    relief="raised",
    fg="#454545",
    font=("IstokWeb Bold", 15 * -1),
    cursor="hand2",
    padx=10,
    pady=10,
    activebackground="light gray",
    activeforeground="black"
)

button_5 = Button(
    text="Stop",
    compound="center",
    command=stop,
    relief="raised",
    fg="#454545",
    font=("IstokWeb Bold", 15 * -1),
    cursor="hand2",
    padx=10,
    pady=10,
    activebackground="light gray",
    activeforeground="black"
)

button_3.place(x=window_width // 2 - 45, y=window_height - footer_height + 15, width=120, height=60)
button_4.place(x=55, y=window_height - footer_height + 15, width=120, height=60)
button_5.place(x=window_width - 145, y=window_height - footer_height + 15, width=120, height=60)

# FOR CAMERA FEED ---------
canvas.place(relx=0, rely=0, relwidth=1, relheight=1 - footer_height / window_height)
window.rowconfigure(0, weight=1)
window.columnconfigure(0, weight=1)

window.bind("<Configure>", update_canvas)
update_canvas()

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Unable to read camera feed")

def update_frame():
    global current_frame, is_running, model
    ret, frame = cap.read()

    if ret:
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        canvas_width = canvas.winfo_width()
        canvas_height = canvas.winfo_height()
        frame_resized = cv2.resize(frame_rgb, (canvas_width, canvas_height))

        current_frame = frame_resized

        if is_running and model is not None:
            result = model(frame_resized, agnostic_nms=True)[0]
            detections = sv.Detections.from_ultralytics(result)

            print(f"Number of detections: {len(detections)}")
            for detection in detections:
                box, _, score, class_id, _, additional_info = detection
                class_name = additional_info['class_name']
                print(f"Detected class: {class_name} with score: {score}, Box: {box}")

            labels = []
            for detection in detections:
                box, _, score, class_id, _, additional_info = detection
                class_name = additional_info['class_name']
                label_text = f"{class_name} - {score:0.2f}"
                labels.append(label_text)

            annotated_frame = box_annotator.annotate(scene=frame_resized, detections=detections)
            frame = label_annotator.annotate(scene=annotated_frame, detections=detections, labels=labels)
            
            zone.trigger(detections=detections)
            frame = zone_annotator.annotate(scene=frame)
        else:
            frame = frame_resized

        img = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(image=img)

        canvas.create_image(0, 0, anchor="nw", image=imgtk)
        canvas.image = imgtk
        
    window.after(10, update_frame)

window.after(10, update_frame)
window.mainloop()

cap.release()
cv2.destroyAllWindows()
