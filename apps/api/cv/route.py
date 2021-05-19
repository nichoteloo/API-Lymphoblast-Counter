import os
from flask import send_from_directory, request, url_for
from werkzeug.utils import secure_filename
from api import app, allowed_file, EXTRACT_DIR, RESULTS_DIR 
from api.utils import handle_upload
from .utils import load_image, faces_extract

@app.route('/api/opencv', methods=['POST'])
def cv_upload():
	if request.method == 'POST':

		## save to upload directory
		file = request.files.get("file")
		dest_folder = app.config['UPLOAD_FOLDER']
		dest_len = len(os.listdir(dest_folder))
		response, status = handle_upload(file, dest_folder, dest_len, return_img_path=True)
		
		## load image from directory path
		img = load_image(response)
		
		## save to extract and result directory
		extract_paths, result_paths = faces_extract(img, save=True, extract=EXTRACT_DIR, result=RESULTS_DIR)
		truncated_extract_path = []
		for path in extract_paths:
			relative_path = path.replace(EXTRACT_DIR, '')
			extract_url = url_for('serve_extract', filename=relative_path)
			truncated_extract_path.append(extract_url) ## relative path to the root

		temp_result_path = result_paths.replace(RESULTS_DIR, '')
		truncated_result_path = url_for('serve_result', filename=temp_result_path)

		return {"extract_path": truncated_extract_path, "result_path":truncated_result_path}, 201

		
		


