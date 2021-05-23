import os
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

## helper function 2
def send_image_req(url,data):
    my_img = {'file': open(data, 'rb')}
    response = requests.post(url, files=my_img)
    return response.json()

# def display():
#     messages = json.loads(request.args['messages'])
#     upload_path = BASE_URL + messages['upload_path']
#     result_path = BASE_URL + messages['result_path']
#     extract_paths = list(map(BASE_URL.__add__, messages['extract_path']))
#     return render_template('result.html', upload_path=upload_path, extract_paths=extract_paths, result_path=result_path)
   
## main routing
# @blueprint.route('/uploaded.html', methods=['POST'])
# def upload_img():
#     url = BASE_URL + '/api/upload'
#     if request.method == 'POST':
#         file = request.files.get('file')
#         data = file.filename
#         response = send_image_req(url,data)
#         saved = response['saved']
#         relative_path = BASE_URL + response['relative_path']

#         if saved:
#             flash('Yey image successfully uploaded and predicted. Result shown below')
#             return render_template('uploaded.html', relative_path=relative_path)
#         else:    
#             flash('Nothing happens so far')
#             return render_template("select.html")
#     return render_template("select.html", message="Your request is not reached")

@blueprint.route('/uploaded.html', methods=['GET','POST'])
def upload_img():
    if request.method == 'POST':
        url = BASE_URL + '/devel/api/upload'
        file = request.files.get('file')
        data = file.filename
        response = send_image_req(url,data)
        saved = response['saved']
        recent_path = BASE_URL + response['recent_upload']
        list_upload = [BASE_URL+x for x in response['list_upload'].values()]

        if saved:
            flash('Yey image successfully uploaded and predicted. All result shown below')
            return render_template('uploaded.html', recent_path=recent_path, list_upload=list_upload)
        else:    
            flash('Nothing happens so far')
            return render_template("select.html")
    elif request.method == 'GET':
        url = BASE_URL + '/storage/uploads'
        response = requests.get(url).json()
        list_upload = [BASE_URL+x for x in response.values()]
        return render_template('uploaded.html', list_upload=list_upload)
    flash("Your request is not reached")
    return render_template("select.html", messages="Your request is not reached")

@blueprint.route('/preprocess', methods=['GET','POST'])
def preprocess_img():
    if request.method == 'POST':
        if 'delete' in request.form:
            filename = str(os.path.basename(request.form.get('upload_path')))
            url = BASE_URL + f'/api/delete_upload/{filename}'
            response = requests.get(url).json()
            if response['delete']:
                list_upload = [BASE_URL+x for x in response["list_upload"].values()]
                flash(f"Image {filename} success deleted")
                return render_template("uploaded.html", messages=f"Image {filename} success deleted", list_upload=list_upload)
        elif 'close' in request.form:
            url = BASE_URL + '/storage/uploads'
            response = requests.get(url).json()
            list_upload = [BASE_URL+x for x in response.values()]
            return render_template('uploaded.html', list_upload=list_upload)
        return 0


