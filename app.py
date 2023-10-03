from flask import Flask, render_template, jsonify
from roboflow import Roboflow
import os

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
