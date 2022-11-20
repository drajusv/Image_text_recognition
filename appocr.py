from __future__ import division, print_function
# coding=utf-8
import sys
import os
import glob
import re
import numpy as np


from skimage import io
from skimage.io import imread
import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"
import easyocr
import cv2
from matplotlib import pyplot as plt
import sys, asyncio

if sys.platform == "win32" and (3, 8, 0) <= sys.version_info < (3, 9, 0):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


# Flask utils
from flask import Flask, redirect, url_for, request, render_template, send_file
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer
print("http://127.0.0.1:5000/")
# Define a flask app
app = Flask(__name__)
file_name = "boxtext.png"
text_file = "readme1.txt"
def model_predict(img_path):
    im = imread(img_path)
    reader = easyocr.Reader(['en'])
    result = reader.readtext(img_path ,paragraph="True")
    
    image = io.imread(img_path)
    img = np.asarray(image)
    spacer = 100
    font = cv2.FONT_HERSHEY_SIMPLEX
    for detection in result: 
        top_left = tuple(detection[0][0])
        bottom_right = tuple(detection[0][2])
        text = detection[1]
        try:
            img = cv2.rectangle(img,top_left,bottom_right,(0,255,0),3)
            img = cv2.putText(img,text,(10,spacer), font, 0.5,(0,100,0),1,cv2.LINE_AA)
            spacer+=15
        except:
            print("cv2err")
        with open('readme1.txt', 'a') as f:
            f.write(text)
            f.close()
    fig = plt.figure(figsize=(10,10))
    #print(img.size)
    plt.imshow(img)
    plt.savefig("boxtext.png")
    
    plt.close()

    return img

@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template("index.html")


@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)
        
        # Make prediction
       
        img = model_predict(file_path)
        
        
        return render_template("index.html", filename = "boxtext.png")
    return None

@app.route ( "/display" )
def display_image(filename=file_name):
    print(filename)
    return send_file(filename, mimetype='image/png')

@app.route ( "/text" )
def display_text(filename= text_file):
    return send_file(filename, mimetype='text/plain')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
