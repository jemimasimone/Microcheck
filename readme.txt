Notes on main.py:

python version 3 or higher should be installed (3.12 yung akin)

on terminal (in directory of Microcheck folder)
- python3 -m venv venv
  (creating python environment)
- source venv/bin/activate OR cd venv/Scripts/activate
  (basta yung path ng activate under venv>bin)
- pip install ultralytics
  (packages like numpy, opencv, torch, pandas, etc. should start downloading after the command)
- pip install supervision
  (for bounding boxes)
- pip install pillow
- pip install sort

use yolo cli to test if installation finished properly
- yolo detect predict model=yolov8l.pt source=0 show=true

To run microcheck.py, on terminal (in directory of Microcheck, after source venv/bin/activate OR cd venv/Scripts/activate):
- python3 microcheck.py

For github commit:
- wag isama venv folder & runs folder & pycache folder
- wag isama yolov8l.pt


To do:
[] filter function - detects only bead || fibre || fragment

(pag ilalagay na custom YOLOv8 model with DCN & attention mechanism)
[] import model, call model
[] fix detection dictionary
[] fix detection labels according to class_names of dataset
[] fix filter detection

(pag ilalagay na model + supervision sa GUI)
[/] fix break function when esc is pressed
[] zoom in and zoom out of camera
[] get filter value of button
