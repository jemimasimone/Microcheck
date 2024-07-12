Notes:

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

use yolo cli to test if installation finished properly
- yolo detect predict model=yolov8l.pt source=0 show=true

To run main.py, on terminal (in directory of Microcheck):
- python3 -m main

For github commit:
- wag isama venv folder & runs folder & pycache folder
- wag isama yolov8l.pt
