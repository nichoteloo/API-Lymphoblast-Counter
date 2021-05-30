import os
from flask import send_from_directory, request, url_for
from werkzeug.utils import secure_filename
from api import app, allowed_file, UPLOAD_DIR, EXTRACT_DIR, RESULTS_DIR, ANNOTATION_PATH, CONFIG_PATH, CHECKPOINT_PATH 
from api.utils import handle_upload
## DEVEL TRIAL
from .utils import load_image, faces_extract
## DEVEL ASLI
# from .utils import LymphoCounterModel


# ####### DEVEL HAMPIR JADI
# @app.route('/api/result/opencv/<filename>', methods=['GET'])
# def result_one_img(filename):
# 	"""
#     func: process to result image
#     input: filename from upload folder
#     output: api call line from result image folder
#     """
# 	if request.method == 'GET':
# 		img_path = UPLOAD_DIR + f"/{filename}"
# 		model = LymphoCounterModel(IMAGE_PATH=img_path, ANNOTATION_PATH=ANNOTATION_PATH, CONFIG_PATH=CONFIG_PATH, CHECKPOINT_PATH=CHECKPOINT_PATH)
# 		result_path = model.detect_image(result=RESULTS_DIR)

# 		result_name = os.path.basename(result_path)
# 		truncated_result_path = url_for('serve_result', filename=result_name)
# 		return {"result_path":truncated_result_path}, 201


###### DEVEL AWAL
@app.route('/api/result/opencv/<filename>', methods=['GET'])
def result_one_img(filename):
	"""
    func: process to result image
    input: filename from upload folder
    output: api call line from result image folder
    """
	if request.method == 'GET':
		img_path = UPLOAD_DIR + f"/{filename}"
		img = load_image(img_path)

		result_paths = faces_extract(img, filename=filename, extract=False, result=True, result_dir=RESULTS_DIR)
		
		result_name = os.path.basename(result_paths)
		truncated_result_path = url_for('serve_result', filename=result_name)
		return {"result_path":truncated_result_path}, 201



########################################################################
########################## Not used ####################################
########################################################################

# @app.route('/api/extract/opencv/<filename>', methods=['GET'])
# def extract_image(filename):
# 	"""
#     func: process to extracted images
#     input: filename for upload folder
#     output: api call line from extracted image folder
#     """
# 	if request.method == 'GET':
# 		img_path = UPLOAD_DIR + f"/{filename}"
# 		img = load_image(img_path)
		
# 		extract_paths, extract_len = faces_extract(img, extract=True, result=False, extract_dir=EXTRACT_DIR)

# 		truncated_extract_path = []
# 		for path in extract_paths:
# 			extract_name = os.path.basename(path)
# 			extract_url = url_for('serve_extract', extract_len=extract_len, filename=extract_name)
# 			truncated_extract_path.append(extract_url) ## relative path to the root
# 		return {"extract_paths": truncated_extract_path}, 201
		
########################################################################
########################## Not used ####################################
########################################################################
		
		


