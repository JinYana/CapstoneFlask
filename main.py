import json
import os
from io import BytesIO
import xml.etree.ElementTree as ET
import lxml
import requests
from lxml import objectify
from PIL import Image
from flask import Flask, request, flash, redirect
from deepface import DeepFace
from werkzeug.utils import secure_filename
import base64

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
    image = request_json.get('image')
    #result = DeepFace.verify(img1_path="img1.jpg", img2_path="img2.jpg")
    imgdata = base64.b64decode(image)
    img = Image.open(BytesIO(imgdata))
    img.show()
    # to jpg
    out_jpg = img.convert("RGB")
    # save file
    out_jpg.save("img1.jpg")
    # filename = secure_filename(file.filename)
    # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    if level == "2":
        url = "http://" + l2temi.ip + ":" + l2temi.port
        dictionary = {'level':level, 'shelfno':shelf, 'bookname':bookname, 'bookid':bookid}
        x = requests.post(url, json.dumps(dictionary), verify=False)

    elif level == "3":
        url = "http://" + l3temi.ip + ":" + l3temi.port
        dictionary = {'level':level, 'shelfno':shelf, 'bookname':bookname, 'bookid':bookid}
        x = requests.post(url, json.dumps(dictionary), verify=False)
    else:
        x = "no result"

    if x == "temi3 is not free":
        url = "http://" + l2temi.ip + ":" + l2temi.port
        x = requests.post(url, "temi is not free", verify=False)



    return "succ"

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
    img.show()
    # to jpg
    out_jpg = img.convert("RGB")
    # save file
    out_jpg.save("img2.jpg")
    result = DeepFace.verify(img1_path="img1.jpg", img2_path="img2.jpg")

    return result

if __name__ == '__main__':
    app.run(host='172.20.10.4', port=105)