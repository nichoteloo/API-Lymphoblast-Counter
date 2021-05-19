import os
import cv2
import numpy as np

# def list_options():
# 	for x in os.listdir(cv2.data.haarcascades):
# 		print(x)

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
		final_dest = os.path.join(extract, f"Extract {extract_len}")
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

	return extract_paths, result_paths
