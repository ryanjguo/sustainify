from flask import Flask, render_template, jsonify
from roboflow import Roboflow
import os
import cv2
import numpy as np

# Load YOLO
def load_yolo():
    net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
    with open("coco.names", "r") as f:
        classes = [line.strip() for line in f.readlines()]
    layers_names = net.getLayerNames()
    output_layers = [layers_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    return net, classes, output_layers

# Function for forward pass, drawing bounding box and showing image
def detect_objects(img, net, outputLayers):  
    blob = cv2.dnn.blobFromImage(img, scalefactor=0.00392, size=(320, 320), mean=(0, 0, 0), swapRB=True, crop=False)
    net.setInput(blob)
    detected_objects = net.forward(outputLayers)
    return detected_objects

app = Flask(__name__)

# Function to download dataset
def download_dataset():
    try:
        rf = Roboflow(api_key=os.environ.get("ROBOFLOW_API_KEY"))  # Use environment variable to store API key
        project = rf.workspace("trash-detection-qzyd2").project("combined-u0h0t")
        dataset = project.version(4).download("yolov8")
        return dataset
    except Exception as e:
        print(f"Error occurred: {e}")
        return None

@app.route('/')
def index():
    dataset = download_dataset()
    if dataset:
        return render_template('index.html', dataset_info="Dataset downloaded successfully.")
    else:
        return render_template('index.html', dataset_info="Failed to download dataset.")

if __name__ == '__main__':
    app.run(debug=True)
