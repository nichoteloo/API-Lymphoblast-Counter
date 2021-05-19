import json
import requests
from threading import Thread
from flask import Flask, redirect, render_template, request, flash, sessions, url_for

app = Flask(__name__)
app.secret_key = b'/R\x99.\xda\xba\x9dD\\.C)f4\x19\x1b\x8b\xa7\x12\xd7\x07\xed\x13\x90'
BASE_URL = 'http://127.0.0.1:5000'

@app.route('/')
def home():
    return render_template('index.html')

def send_image_req(url,data):
    my_img = {'file': open(data, 'rb')}
    response = requests.post(url, files=my_img)
    return response.json()

@app.route('/', methods=['POST'])
def predict_image():
    url = BASE_URL + '/api/opencv'

    if request.method == 'POST':
        file = request.files.get('file')
        data = file.filename
        response = send_image_req(url,data)

        saved = response['saved']

        if saved:
            flash('Yey image successfully uploaded and predicted. Result shows below')
            return redirect(url_for('display', messages=json.dumps(response)))
        else:    
            flash('Nothing happens so far')
            return render_template("index.html",)
    
    return render_template("index.html", message="Your request is not reached")

@app.route('/display')
def display():
    messages = json.loads(request.args['messages'])
    upload_path = BASE_URL + messages['upload_path']
    result_path = BASE_URL + messages['result_path']
    extract_paths = list(map(BASE_URL.__add__, messages['extract_path']))
    # import pdb; pdb.set_trace()
    return render_template('display.html', upload_path=upload_path, extract_paths=extract_paths, result_path=result_path)
    
if __name__ == "__main__":
    app.run(port=5001, debug=True)