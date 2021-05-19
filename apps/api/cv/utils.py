import os
import cv2
import numpy as np

# def list_options():
# 	for x in os.listdir(cv2.data.haarcascades):
# 		print(x)

def get_cascade(cascade='haarcascade_frontalface_default.xml'):
	return os.path.join(cv2.data.haarcascades, cascade)

def load_image(image_path):
	frame = cv2.imread(image_path)
	return frame

def faces_extract(frame, save=True, destination=None, result=None):

	## load model
	cascade_xml = get_cascade()
	cascade = cv2.CascadeClassifier(cascade_xml)

	## preprocess image from frame
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	faces = cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5, minSize=(30, 30))

	## check for destination directory
	final_dest = None
	if destination is not None:
		list_count = len(os.listdir(destination)) + 1
		final_dest = os.path.join(destination, f"Extract {list_count}")
		os.makedirs(final_dest, exist_ok=True)

	## bounding box coordinate checking
	paths = []
	for i, (x, y, w, h) in enumerate(faces):
		## create bounding box
		cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 255), 2)
		## for counter
		roi_color = frame[y:y+h, x:x+w]
		if save == True and destination != None:
			current_path = os.path.join(final_dest, f"{i}.jpg")
			cv2.imwrite(current_path, roi_color)
			paths.append(current_path)

	list_count = len(os.listdir(result)) + 1
	final_path = os.path.join(result, f"{list_count }.jpg")
	status = cv2.imwrite(final_path, frame)

	return paths
