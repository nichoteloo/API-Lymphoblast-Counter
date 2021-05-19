import os
from flask import send_from_directory, request, url_for
from werkzeug.utils import secure_filename
from api import app, allowed_file, OUTPUTS_DIR, RESULTS_DIR 
from .utils import load_image, faces_extract

@app.route('/api/opencv', methods=['POST'])
def handle_cv_upload():
	if request.method == 'POST':

		if 'file' not in request.files:
			return {"detail": "No file part"}, 400

		file = request.files['file']
		if file.filename == '':
			return {"detail": "No image selected for uploading"}, 400

		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename) # security purpose
			_, ext = os.path.splitext(filename) # take extension

			destination_folder = app.config['UPLOAD_FOLDER']
			new_filename = f"{len(os.listdir(destination_folder)) + 1}{ext}" # set new filename

			save_path = os.path.join(destination_folder, new_filename)

			file.save(save_path)

			img = load_image(save_path)
			
			paths = faces_extract(img, save=True, destination=OUTPUTS_DIR, result=RESULTS_DIR)
			response_paths = []
			for path in paths:
				relative_path = path.replace(OUTPUTS_DIR, '')
				extract_url = url_for('serve_extract', filename=relative_path)
				response_paths.append(extract_url)

			return {"paths": response_paths}, 201
		else:
			return {"detail": "Allowed image types are - png, jpg, jpeg"}, 401

		
		


