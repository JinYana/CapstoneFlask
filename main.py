import json
import os
from io import BytesIO
import xml.etree.ElementTree as ET
import lxml
from lxml import objectify
from PIL import Image
from flask import Flask, request, flash, redirect
from deepface import DeepFace
from werkzeug.utils import secure_filename
import base64
import requests
import os
from io import BytesIO
import xml.etree.ElementTree as ET
import lxml
from lxml import objectify
from PIL import Image
from flask import Flask, request, flash, redirect
from deepface import DeepFace
from werkzeug.utils import secure_filename
import base64
import requests
import cv2
import matplotlib.pyplot as plt

class Client:
    name = ""
    ip = ""
    port = ""

addresses = ET.parse('addresses.xml')
root = addresses.getroot()
l3temi = Client()
l2temi = Client()
for child in root:
    if child[0].text == "TemiL3":
        l3temi.name = child[0].text
        l3temi.ip = child[1].text
        l3temi.port = child[2].text
    elif child[0].text == "TemiL2 (phone)":
        l2temi.name = child[0].text
        l2temi.ip = child[1].text
        l2temi.port = child[2].text

app = Flask(__name__)
# UPLOAD_FOLDER = '/CapstoneFlask'
# ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
#
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/wronglevel', methods=['POST'])
def wronglevel():
    request_json = request.get_json()
    level = request_json.get('level')
    shelf = request_json.get('shelfno')
    bookname = request_json.get('bookname')
    bookid = request_json.get('bookid')
    
    dictToSend = {'level':level,
                  "shelfno": shelf,
                  "bookid": bookid,
                  "bookname": bookname}
    
    url = "http://172.20.10.6:8080"
    url = "http://192.168.43.145:8080"
    res = requests.post(url, json=dictToSend)
    print("reponse from server:", res.text)

    dictToSend = {'response': res.text,
                  'response_code': res.status_code}
    return json.dump(dictToSend)

    #dictFromServer = res.json()
        
    # image = request_json.get('image')
    #result = DeepFace.verify(img1_path="img1.jpg", img2_path="img2.jpg")
    # imgdata = base64.b64decode(image)
    # img = Image.open(BytesIO(imgdata))
    # img.show()
    # to jpg
    # Out_jpg = img.convert("RGB")
    # save file
    # out_jpg.save("img1.jpg")
    # filename = secure_filename(file.filename)
    # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    

# Image 1
@app.route('/receiveimage', methods=["POST"])
def receivedImage():
    request_json = request.get_json()
    image = request_json.get('image')
    imgdata = base64.b64decode(image)
    img = Image.open(BytesIO(imgdata))
    out_jpg = img.convert("RGB")
    
    # save file
    out_jpg.save("img1.jpg")
    
    # filename = secure_filename(file.filename)
    # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    
    return None

# Image 2
@app.route('/faceverification', methods=['POST'])
def faceverification():
    request_json = request.get_json()
    # level = request_json.get('level')
    # shelf = request_json.get('shelfno')
    # bookname = request_json.get('bookname')
    # bookid = request_json.get('bookid')
    image = request_json.get('image')

    imgdata = base64.b64decode(image)
    img = Image.open(BytesIO(imgdata))
    # to jpg
    out_jpg = img.convert("RGB")
    # save file
    out_jpg.save("img2.jpg")
    
    
    output = DeepFace.verify("img1.jpg","img2.jpg")
    verification = output['verified']
    if verification:
        print("they are same")
        
    else:
       print("they are not the same")
       
    return None

if __name__ == '__main__':
    app.run(host='192.168.43.244', port=8080)