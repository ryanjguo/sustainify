from flask import Flask, render_template, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
from roboflow import Roboflow
import os
import json
import base64


app = Flask(__name__)

rf = Roboflow(api_key=os.environ.get("ROBOFLOW_API_KEY"))
project = rf.workspace().project("garbage-classification-3")
model = project.version(2).model

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        print('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        print('No selected file')
        return redirect(request.url)
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join('uploads', filename)
        file.save(filepath)
        
        # Make prediction
        prediction = model.predict(filepath, confidence=40, overlap=30).json()
        prediction_json = json.dumps(prediction, indent=4)  # Format prediction as JSON string for display

        return render_template('results.html', filename=filename, prediction=prediction_json)
    
@app.route('/upload-webcam', methods=['POST'])
def upload_webcam():
    image_data = request.form['imageData'].split(',')[1]  # Get the data part of the image
    image_data = base64.b64decode(image_data)  # Decode the base64 image data

    image_path = 'image.png'
    # Save the image to a file
    with open(image_path, 'wb') as image_file:
        image_file.write(image_data)

    # Now you can process the image with your model
    prediction = model.predict(image_path, confidence=40, overlap=30).json()

    # Render the results template with the predictions
    return render_template('results.html', prediction=prediction)


@app.route('/')
def index():
    return render_template('index.html')

if not os.path.exists('uploads'):
    os.makedirs('uploads')

if __name__ == '__main__':
    app.run(debug=True)

