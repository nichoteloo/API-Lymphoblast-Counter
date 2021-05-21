import os
from flask import send_from_directory, request
from api import app
from .utils import handle_upload

@app.route("/storage/uploads/<filename>")
def serve_upload(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/storage/results/<filename>')
def serve_result(filename):
    return send_from_directory(app.config['RESULTS_DIR'], filename)

@app.route('/storage/extract/<extract_len>/<filename>')
def serve_extract(extract_len, filename):
    return send_from_directory(app.config['EXTRACT_DIR'], f'Extract_{extract_len}/' + filename, mimetype='image/jpg')








        