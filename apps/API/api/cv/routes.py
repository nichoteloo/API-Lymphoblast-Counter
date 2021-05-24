import os
from flask import send_from_directory, request, url_for
from werkzeug.utils import secure_filename
from api import app, allowed_file, UPLOAD_DIR, EXTRACT_DIR, RESULTS_DIR 
from api.utils import handle_upload
from .utils import load_image, faces_extract


@app.route('/devel2/api/opencv/<filename>', methods=['GET','POST'])
def devel_cv_upload_2(filename):
	if request.method == 'GET':
		img_path = UPLOAD_DIR + f"/{filename}"
		img = load_image(img_path)

		extract_paths, result_paths, extract_len = faces_extract(img, save=True, extract=EXTRACT_DIR, result=RESULTS_DIR)
		truncated_extract_path = []
		for path in extract_paths:
			extract_name = os.path.basename(path)
			extract_url = url_for('serve_extract', extract_len=extract_len, filename=extract_name)
			truncated_extract_path.append(extract_url) ## relative path to the root
		
		result_name = os.path.basename(result_paths)
		truncated_result_path = url_for('serve_result', filename=result_name)
		return {"extract_path": truncated_extract_path, "result_path":truncated_result_path}, 201


@app.route('/devel/api/opencv', methods=['POST'])
def devel_cv_upload():
	if request.method == 'POST':
		## convert rel_path to img_path
		path = request.json.get("rel_path")
		basename = os.path.basename(path)
		img_path = UPLOAD_DIR + f"/{basename}"
		
		img = load_image(img_path)

		## save to extract and result directory
		extract_paths, result_paths, extract_len = faces_extract(img, save=True, extract=EXTRACT_DIR, result=RESULTS_DIR)
		truncated_extract_path = []
		for path in extract_paths:
			# filename = path.replace(EXTRACT_DIR + f'/Extract_{extract_len}', '')
			extract_name = os.path.basename(path)
			extract_url = url_for('serve_extract', extract_len=extract_len, filename=extract_name)
			truncated_extract_path.append(extract_url) ## relative path to the root
		
		# temp_result_path = result_paths.replace(RESULTS_DIR, '')
		result_name = os.path.basename(result_paths)
		truncated_result_path = url_for('serve_result', filename=result_name)
		# import pdb;pdb.set_trace()
		return {"extract_path": truncated_extract_path, "result_path":truncated_result_path}, 201


@app.route('/api/opencv', methods=['POST'])
def cv_upload():
	if request.method == 'POST':

		## save to upload directory
		file = request.files.get("file")
		dest_folder = app.config['UPLOAD_FOLDER']
		dest_len = len(os.listdir(dest_folder))
		response, img_path, status = handle_upload(file, dest_folder, dest_len, return_img_path=True)

		## load image from directory path
		img = load_image(img_path)
		
		## save to extract and result directory
		extract_paths, result_paths, extract_len = faces_extract(img, save=True, extract=EXTRACT_DIR, result=RESULTS_DIR)
		truncated_extract_path = []
		for path in extract_paths:
			filename = path.replace(EXTRACT_DIR + f'/Extract_{extract_len}', '')
			extract_url = url_for('serve_extract', extract_len=extract_len, filename=filename)
			truncated_extract_path.append(extract_url) ## relative path to the root

		temp_upload_path = img_path.replace(UPLOAD_DIR, '')
		truncated_upload_path = url_for('serve_upload', filename=temp_upload_path)
		
		temp_result_path = result_paths.replace(RESULTS_DIR, '')
		truncated_result_path = url_for('serve_result', filename=temp_result_path)

		return {"saved": response['saved'], "upload_path":truncated_upload_path, 
				"extract_path": truncated_extract_path, "result_path":truncated_result_path}, 201

		
		


