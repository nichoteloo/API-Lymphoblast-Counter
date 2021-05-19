import os
from flask import send_from_directory, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from api import app, allowed_file

@app.route('/api/upload', methods=['POST'])
def upload_file():
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
			return {"detail": "Image successfully uploaded"}, 200
		else:
			return {"detail": "Allowed image types are - png, jpg, jpeg"}, 401







        