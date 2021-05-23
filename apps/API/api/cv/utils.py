import os
import cv2
import numpy as np

############################################################################################################

# import tensorflow as tf
# from api import WORKSPACE_PATH, ANNOTATION_PATH, MODEL_PATH, CONFIG_PATH, CHECKPOINT_PATH
# from object_detection.utils import label_map_util
# from object_detection.utils import visualization_utils as viz_utils
# from object_detection.builders import model_builder
# from object_detection.utils import config_util
# from object_detection.protos import pipeline_pb2
# from google.protobuf import text_format

############################################################################################################

# def load_config(CONFIG_PATH):
#     configs = config_util.get_configs_from_pipeline_file(CONFIG_PATH + "/pipeline.config")
#     detection_model = model_builder.build(model_config=configs['model'], is_training=False)
#     return detection_model

# def restore_chk(detection_model, CHECKPOINT_PATH):
#     ckpt = tf.compat.v2.train.Checkpoint(model=detection_model)
#     ckpt.restore(CHECKPOINT_PATH + "/ckpt-9").expect_partial()
#     return ckpt

# def cat_index(ANNOTATION_PATH):
#     return label_map_util.create_category_index_from_labelmap(ANNOTATION_PATH + "/label_map.pbtxt")

# def load_image(image_path):
#     frame = cv2.imread(image_path)
#     frame_np = np.array(frame) 
#     return frame_np

# @tf.function
# def detect_fn(image):
#     image, shapes = detection_model.preprocess(image)
#     prediction_dict = detection_model.predict(image, shapes)
#     detections = detection_model.postprocess(prediction_dict, shapes)
#     return detections

# def detect_image(frame, label_id_offset=1, save=True, extract=None, result=None):
# 	input_tensor = tf.convert_to_tensor(np.expand_dims(frame, 0), dtype=tf.float32)
# 	detections = detect_fn(input_tensor)

# 	num_detections = int(detections.pop('num_detections'))
# 	detections = {key: value[0, :num_detections].numpy() for key, value in detections.items()}
# 	detections['num_detections'] = num_detections

# 	# detection_classes should be ints.
# 	detections['detection_classes'] = detections['detection_classes'].astype(np.int64)

# 	image_np_with_detections = frame.copy()
    
# 	image_np_with_detections = viz_utils.visualize_boxes_and_labels_on_image_array(
# 									image_np_with_detections,
# 									detections['detection_boxes'],
# 									detections['detection_classes']+label_id_offset,
# 									detections['detection_scores'],
# 									category_index,
# 									use_normalized_coordinates=True,
# 									max_boxes_to_draw=20,
# 									min_score_thresh=.5,
# 									agnostic_mode=False)

# 	## check for extract directory
# 	final_dest = None
# 	if extract is not None:
# 		extract_len = len(os.listdir(extract)) + 1
# 		final_dest = os.path.join(extract, f"Extract_{extract_len}")
# 		os.makedirs(final_dest, exist_ok=True)

# 	## bounding box coordinate checking
# 	extract_paths = [] 
# 	for i, (x, y, w, h) in enumerate(faces):
# 		## create bounding box
# 		cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
# 		## for counter
# 		roi_color = frame[y:y+h, x:x+w]
# 		if save == True and extract != None:
# 			current_path = os.path.join(final_dest, f"{i+1}.jpg")
# 			cv2.imwrite(current_path, roi_color)
# 			extract_paths.append(current_path)

# 	result_len = len(os.listdir(result)) + 1
# 	result_paths = os.path.join(result, f"{result_len}.jpg")
# 	status = cv2.imwrite(result_paths, image_np_with_detections)

# 	return extract_paths, result_paths, extract_len


############################################################################################################

def list_options():
	for x in os.listdir(cv2.data.haarcascades):
		print(x)

def get_cascade(cascade_xml='haarcascade_frontalface_default.xml'):
	cascade_path = os.path.join(cv2.data.haarcascades, cascade_xml)
	cascade = cv2.CascadeClassifier(cascade_path)
	return cascade

def load_image(image_path):
	frame = cv2.imread(image_path)
	return frame

def faces_extract(frame, save=True, extract=None, result=None):

	## load model
	cascade = get_cascade()

	## preprocess image from frame
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	faces = cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5, minSize=(30, 30))

	## check for extract directory
	final_dest = None
	if extract is not None:
		extract_len = len(os.listdir(extract)) + 1
		final_dest = os.path.join(extract, f"Extract_{extract_len}")
		os.makedirs(final_dest, exist_ok=True)

	## bounding box coordinate checking
	extract_paths = [] 
	for i, (x, y, w, h) in enumerate(faces):
		## create bounding box
		cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
		## for counter
		roi_color = frame[y:y+h, x:x+w]
		if save == True and extract != None:
			current_path = os.path.join(final_dest, f"{i+1}.jpg")
			cv2.imwrite(current_path, roi_color)
			extract_paths.append(current_path)

	result_len = len(os.listdir(result)) + 1
	result_paths = os.path.join(result, f"{result_len}.jpg")
	status = cv2.imwrite(result_paths, frame)

	return extract_paths, result_paths, extract_len
