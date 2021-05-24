import os
import json
import requests
from decouple import config
from flask import Flask, redirect, render_template, request, flash, sessions, url_for

app = Flask(__name__)
app.secret_key = config('SECRET_KEY')
BASE_URL = 'http://127.0.0.1:8000'

###################### HELPER ############################################################
def serve_endpoint(path):
    return BASE_URL + path

def send_image_req(url,data):
    my_img = {'file': open(data, 'rb')}
    response = requests.post(url, files=my_img)
    return response.json()

def send_path_req(url, path):
    param = {'rel_path': path}
    response = requests.post(url, json=param)
    return response.json()

##########################################################################################
################### MAIN ROUTING #########################################################
############## ONLY FOR TESTING API ######################################################
##########################################################################################

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def upload_image():
    if request.method == 'POST':
        file = request.files.get('file')
        data = file.filename
        response = send_image_req(serve_endpoint('/api/upload'),data)
        saved = response['saved']
        recent_upload = serve_endpoint(response['recent_upload'])
        
        if saved:
            flash('Yey image successfully uploaded and predicted. Result shows below')
            return render_template('index.html', recent_upload=recent_upload)
        else:    
            flash('Nothing happens so far')
            return render_template("index.html")
    return render_template("index.html", message="Your request is not reached")

@app.route('/predict', methods=['POST'])
def predict_img():
    if request.method == 'POST':
        recent_upload = request.form.get('recent_upload')
        base_up = os.path.basename(recent_upload)

        response_res = requests.get(serve_endpoint(f'/api/result/opencv/{base_up}')).json()
        response_ext = requests.get(serve_endpoint(f'/api/extract/opencv/{base_up}')).json()
        # response = {response_res, response_ext}
        return redirect(url_for('display', response_res=json.dumps(response_res), 
                    response_ext=json.dumps(response_ext)))
        
@app.route('/display')
def display():
    messages_res = json.loads(request.args['response_res'])
    messages_ext = json.loads(request.args['response_ext'])
    result_path = serve_endpoint(messages_res['result_path'])
    extract_paths = list(map(BASE_URL.__add__, messages_ext['extract_paths']))
    
    return render_template('display.html', extract_paths=extract_paths, result_path=result_path)

##########################################################################################
##########################################################################################
##########################################################################################

if __name__ == "__main__":
    app.run(port=5001, debug=True)