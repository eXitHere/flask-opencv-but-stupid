from flask import Flask, request, Response, jsonify
from flask_cors import CORS
import numpy as np
import cv2
import matplotlib.pyplot as plt
import time
from PIL import Image
import os , io , sys
import base64

app = Flask(__name__)
CORS(app)

cascPath = 'detect/haarcascade_frontalface_alt.xml'
faceCascade = cv2.CascadeClassifier(cascPath)

# route http posts to this method
@app.route('/api/test', methods=['POST'])
def test():
    # print(request.files , file=sys.stderr)
    file = request.files['image'].read() ## byte file
    npimg = np.fromstring(file, np.uint8)
    img = cv2.imdecode(npimg,cv2.COLOR_BGR2RGB)
    # gray = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    faces = faceCascade.detectMultiScale(
        img,
        scaleFactor=1.1,
        minNeighbors=6,
        minSize=(40, 40),
        flags = cv2.CASCADE_SCALE_IMAGE
    )
    print("Found %d faces!" % len(faces))

    face = faces[0]
    (y, x, w, h) = face
    face_master = img[x:x+w, y:y+h]

    for (y, x, w, h) in faces:
      img[x:x+w, y:y+h] = cv2.resize(face_master, (w, h), interpolation = cv2.INTER_AREA)
        # cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 4)
    # plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    img = Image.fromarray(img.astype("uint8"))
    rawBytes = io.BytesIO()
    img.save(rawBytes, "JPEG")
    rawBytes.seek(0)
    img_base64 = base64.b64encode(rawBytes.read())
    return jsonify({'status':str(img_base64)})

@app.route("/")
def index():
  return "Hello World"