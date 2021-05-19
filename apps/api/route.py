import os
from flask import send_from_directory, request
from api import app
from .utils import handle_upload

@app.route("/static/uploads/<filename>")
def static_uploads_view(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/static/results/<filename>')
def serve_result(filename):
    return send_from_directory(app.config['RESULTS_DIR'], filename)

@app.route('/static/extract/<filename>')
def serve_extract(filename):
	return send_from_directory(app.config['EXTRACT_DIR'], filename)

@app.route("/api/upload", methods=["POST"])
def api_upload():
	if request.method == "POST":
		file = request.files.get("file")
		dest = app.config['UPLOAD_FOLDER']
		dest_len = len(os.listdir(dest))
		return handle_upload(file, dest, dest_len)
	return {"detail": "Not allowed"}, 400









        