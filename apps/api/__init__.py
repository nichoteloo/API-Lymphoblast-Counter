import os 
from flask import Flask, flash, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename

## setting up first
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "storage", "uploads")
EXTRACT_DIR = os.path.join(BASE_DIR, "storage", "extract")
RESULTS_DIR = os.path.join(BASE_DIR, "storage", "results")

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

for d in [UPLOAD_DIR, RESULTS_DIR, EXTRACT_DIR]:
	os.makedirs(d, exist_ok=True)

app = Flask(__name__)
app.secret_key = b'/R\x99.\xda\xba\x9dD\\.C)f4\x19\x1b\x8b\xa7\x12\xd7\x07\xed\x13\x90'
app.config['EXTRACT_DIR'] = EXTRACT_DIR # store the result
app.config['UPLOAD_FOLDER'] = UPLOAD_DIR # directly from the source
app.config['RESULTS_DIR'] = RESULTS_DIR

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

from .route import *
from .cv.route import *