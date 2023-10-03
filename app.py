from flask import Flask, render_template, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
from roboflow import Roboflow
import os
import json
import base64
import openai

app = Flask(__name__)

rf = Roboflow(api_key=os.environ.get("ROBOFLOW_API_KEY"))
project = rf.workspace().project("garbage-classification-3")
model = project.version(2).model

openai.api_key = os.getenv('OPENAI_API_KEY')

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

        object_type = prediction['predictions'][0]['class']
        prompt = f"How should I properly dispose of {object_type} waste?"
        
        response = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",
        prompt=prompt,
        temperature=0.5,
        max_tokens=200,
        top_p=0.5
    )

        disposal_instruction = response.choices[0].text.strip()

        return render_template('results.html', filename=filename, prediction=prediction, disposal_instruction=disposal_instruction)
    
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

    object_type = prediction['predictions'][0]['class']
    prompt = f"How to properly dispose of {object_type} waste? Provide clear and concise steps or methods that are environmentally friendly and widely acceptable. Avoid repetitive or overly general advice. [max tokens=200]"

    response = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",
        prompt=prompt,
        temperature=0.5,
        max_tokens=200,
        top_p=0.5
    )
    
    disposal_instruction = response.choices[0].text.strip()

    # Return the results as JSON
    return render_template('results.html', prediction=prediction, disposal_instruction=disposal_instruction)

@app.route('/')
def index():
    return render_template('index.html')

if not os.path.exists('uploads'):
    os.makedirs('uploads')

if __name__ == '__main__':
    app.run(debug=True)

