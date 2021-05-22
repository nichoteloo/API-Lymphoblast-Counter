import json
import requests
from app.home import blueprint
from flask import render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app import login_manager
from jinja2 import TemplateNotFound

BASE_URL = 'http://127.0.0.1:8000'

@blueprint.route('/index')
@login_required
def index():
    return render_template('index.html', segment='index')

@blueprint.route('/<template>')
@login_required
def route_template(template):
    try:

        if not template.endswith( '.html' ):
            template += '.html'

        # Detect the current page
        segment = get_segment( request )

        # Serve the file (if exists) from app/templates/FILE.html
        return render_template( template, segment=segment )

    except TemplateNotFound:
        return render_template('page-404.html'), 404
    
    except:
        return render_template('page-500.html'), 500

# Helper - Extract current page name from request 
def get_segment( request ): 

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment    

    except:
        return None  

def send_image_req(url,data):
    my_img = {'file': open(data, 'rb')}
    response = requests.post(url, files=my_img)
    return response.json()

@blueprint.route('/select.html', methods=['POST'])
def upload_img():
    if request.method == 'POST':
        upload = request.files.get('file')
        data = file.filename
        response = send_image_req(url,data)

@blueprint.route('/uploaded.html', methods=['POST'])
def predict_image():
    url = BASE_URL + '/api/opencv'
    if request.method == 'POST':
        file = request.files.get('file')
        data = file.filename
        response = send_image_req(url,data)
        saved = response['saved']
        relative_path = BASE_URL + response['relative_path']

        if saved:
            flash('Yey image successfully uploaded and predicted. Result shows below')
            return render_template('uploaded.html', relative_path=relative_path)
        else:    
            flash('Nothing happens so far')
            return render_template("select.html",)
    return render_template("select.html", message="Your request is not reached")

def display():
    messages = json.loads(request.args['messages'])
    upload_path = BASE_URL + messages['upload_path']
    result_path = BASE_URL + messages['result_path']
    extract_paths = list(map(BASE_URL.__add__, messages['extract_path']))
    return render_template('result.html', upload_path=upload_path, extract_paths=extract_paths, result_path=result_path)
   
