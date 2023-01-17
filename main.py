import os
from io import BytesIO

from PIL import Image
from flask import Flask, request, flash, redirect
from deepface import DeepFace
from werkzeug.utils import secure_filename
import base64


app = Flask(__name__)
# UPLOAD_FOLDER = '/CapstoneFlask'
# ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
#
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/wronglevel', methods=['POST'])
def wronglevel():
    request_json = request.get_json()
    # level = request_json.get('level')
    # shelf = request_json.get('shelfno')
    # bookname = request_json.get('bookname')
    # bookid = request_json.get('bookid')
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
    return

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