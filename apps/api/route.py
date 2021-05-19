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

@app.route('/storage/extract/<filename>')
def serve_extract(filename):
    import pdb; pdb.set_trace()
    return send_from_directory(app.config['EXTRACT_DIR'], 'Extract%201', filename)








        