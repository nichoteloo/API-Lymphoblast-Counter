import os
from flask import send_from_directory, request, url_for
from api import app, UPLOAD_DIR
from .utils import handle_upload

####################################################################
## For basic functionality, upload, delete, and retrieve specific 
##image, and retrieve all image from its respective folder
####################################################################

@app.route("/storage/uploads", methods=['GET'])
def list_upload_file():
    """
    func: retrieve all images in uploads folder directory
    input: none
    output: api call line to retrieve image
    """
    list_of_files = {}
    for i, filepath in enumerate(os.listdir(UPLOAD_DIR)):
        filename = os.path.basename(filepath)
        list_of_files[i+1] = url_for('serve_upload', filename=filename)
    return list_of_files

@app.route("/storage/uploads/<filename>")
def serve_upload(filename):
    """
    func: retrieve specific image from its directory
    input: filename
    output: api call line for rendering image
    """
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/storage/results/<filename>')
def serve_result(filename):
    """
    func: retrieve result image from its directory
    input: filename
    output: api call line for rendering image
    """
    return send_from_directory(app.config['RESULTS_DIR'], filename)

@app.route('/storage/extract/<extract_len>/<filename>')
def serve_extract(extract_len, filename):
    """
    func: retrieve extracted images from its directory
    input: length of extract folder (for update folder name), filename
    output: api call line for rendering image
    """
    return send_from_directory(app.config['EXTRACT_DIR'], f'Extract_{extract_len}/' + filename, mimetype='image/jpg')

@app.route('/api/upload', methods=['POST'])
def api_upload():
    """
    func: upload image from local directory to upload folder
    input: none
    output: json, contains api call line for current image and all images in upload directory
    """
    if request.method == "POST":
        ## save to upload directory
        file = request.files.get("file")
        dest_folder = app.config['UPLOAD_FOLDER']
        response, status = handle_upload(file, dest_folder, return_img_path=True)
        # import pdb; pdb.set_trace()
        jpgname = os.path.basename(response['save_path'])
        recent_upload = url_for('serve_upload', filename=jpgname)
        list_upload = list_upload_file()
        return {"saved": response['saved'], "recent_upload":recent_upload, "list_upload": list_upload}, status
    return {"detail":"Upload failed"}, 400

@app.route('/api/delete_upload/<filename>', methods=['GET'])
def delete_upload(filename):
    """
    func: delete image
    input: filename
    output: detail, api call line for all images in upload directory
    """
    if request.method == "GET":
        filepath = UPLOAD_DIR + f'/{filename}'
        if os.path.isfile(filepath):
            os.remove(filepath)
            list_upload = list_upload_file()
            return {"delete":True, "list_upload":list_upload}
        return {"detail":"File is not in directory", "list_upload":list_upload}
    return {"detail":"Request not reached", "list_upload":list_upload}




        