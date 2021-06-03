import os
from flask import send_from_directory, request, url_for
from werkzeug.utils import secure_filename
from api import app, allowed_file, UPLOAD_DIR, EXTRACT_DIR, RESULTS_DIR, ANNOTATION_PATH, CONFIG_PATH, CHECKPOINT_PATH 
from api.utils import handle_upload
from .utils import LymphoCounterModel

@app.route('/api/result/opencv/<filename>', methods=['GET'])
def result_one_img(filename):
	"""
    func: process to result image
    input: filename from upload folder
    output: api call line from result image folder
    """
	if request.method == 'GET':
		img_path = UPLOAD_DIR + f"/{filename}"
		model = LymphoCounterModel(IMAGE_PATH=img_path, ANNOTATION_PATH=ANNOTATION_PATH, CONFIG_PATH=CONFIG_PATH, CHECKPOINT_PATH=CHECKPOINT_PATH)
		result_path = model.detect_image(result=RESULTS_DIR)

		result_name = os.path.basename(result_path)
		truncated_result_path = url_for('serve_result', filename=result_name)
		return {"result_path":truncated_result_path}, 201