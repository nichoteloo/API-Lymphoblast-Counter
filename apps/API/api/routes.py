import os
from flask import send_from_directory, request, url_for
from api import app, UPLOAD_DIR
from .utils import handle_upload

@app.route("/storage/uploads", methods=['GET'])
def list_upload_file():
    list_of_files = {}
    for i, filepath in enumerate(os.listdir(UPLOAD_DIR)):
        filename = os.path.basename(filepath)
        list_of_files[i+1] = url_for('serve_upload', filename=filename)
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

@app.route('/devel/api/upload', methods=['POST'])
def api_upload_devel():
    if request.method == "POST":
        ## save to upload directory
        file = request.files.get("file")
        dest_folder = app.config['UPLOAD_FOLDER']
        dest_len = len(os.listdir(dest_folder))
        response, img_path, status = handle_upload(file, dest_folder, dest_len, return_img_path=True)
        jpgname = os.path.basename(img_path)
        recent_upload = url_for('serve_upload', filename=jpgname)
        list_upload = list_upload_file()
        return {"saved": response['saved'], "recent_upload":recent_upload, "list_upload": list_upload}, 201
    return {"detail":"Upload failed"}, 400

@app.route('/api/delete_upload/<filename>', methods=['GET'])
def delete_upload(filename):
    if request.method == "GET":
        filepath = UPLOAD_DIR + f'/{filename}'
        if os.path.isfile(filepath):
            os.remove(filepath)
            list_upload = list_upload_file()
            return {"delete":True, "list_upload":list_upload}
        return {"detail":"File is not in directory", "list_upload":list_upload}
    return {"detail":"Request not reached", "list_upload":list_upload}




        