from flask import Flask, request
from deepface import DeepFace
app = Flask(__name__)


@app.route('/wronglevel', methods=['POST'])
def hello():
    request_json = request.get_json()
    level = request_json.get('level')
    shelf = request_json.get('shelfno')
    bookname = request_json.get('bookname')
    bookid = request_json.get('bookid')

    return

if __name__ == '__main__':
    app.run(host='172.20.10.4', port=105)