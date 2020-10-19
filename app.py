from flask import Flask,render_template,redirect,url_for,flash,request,jsonify
import os
from werkzeug.utils import secure_filename
import json
import numpy as np
import cv2
from PIL import Image
import requests

app=Flask(__name__)
app.config['SECRET_KEY']="ankit"

MODEL_URI='http://localhost:8502/v1/models/pets:predict'

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route("/prediction",methods=['POST'])
def getPrediction():
    print("getting predictions")
    print(request.form)
    print(request.files['image'])

    # read image file string data

    img = Image.open(request.files['image'])
    img = np.array(img)
    img = cv2.resize(img, (128, 128))
    # img = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2GRAY)
    # image = np.expand_dims(img, axis=0)
    image=img
    print(image.shape)
    # inp=tf.convert_to_tensor(image)

    data = json.dumps({"instances":    [image.tolist(),image.tolist()] })
    response = requests.post(MODEL_URI, data=data.encode())
    result = json.loads(response.text)
    print(result['predictions'][0])
    res=""

    if(result['predictions'][0][0]>result['predictions'][0][1]):
        res="cat"
    else:
        res="dog"
    return jsonify(prediction=res)

if __name__=='__main__':
    app.run(debug=True)