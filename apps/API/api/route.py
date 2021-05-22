import os
from flask import send_from_directory, request, url_for
from api import app, UPLOAD_DIR
from .utils import handle_upload

@app.route("/storage/uploads")
def list_upload():
    list_of_files = {}
    for filename in os.listdir(UPLOAD_DIR):
        list_of_files[filename] = UPLOAD_DIR + f"/{filename}"
    return list_of_files

@app.route("/storage/uploads/<filename>")
def serve_upload(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/storage/results/<filename>')
def serve_result(filename):
    return send_from_directory(app.config['RESULTS_DIR'], filename)

@app.route('/storage/extract/<extract_len>/<filename>')
def serve_extract(extract_len, filename):
    return send_from_directory(app.config['EXTRACT_DIR'], f'Extract_{extract_len}/' + filename, mimetype='image/jpg')

@app.route('/api/upload', methods=['POST'])
def api_upload():
    if request.method == "POST":
        ## save to upload directory
        file = request.files.get("file")
        dest_folder = app.config['UPLOAD_FOLDER']
        dest_len = len(os.listdir(dest_folder))
        response, img_path, status = handle_upload(file, dest_folder, dest_len, return_img_path=True)
        jpgname = os.path.basename(img_path)
        relative_path = url_for('serve_upload', filename=jpgname)
        return {"saved": response['saved'], "relative_path":relative_path}, 201
    return {"detail":"Upload failed"}, 400





        