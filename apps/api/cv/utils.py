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
	# frame = cv2.cv.LoadImage(image_path)
	import pdb; pdb.set_trace()
	return frame

def faces_extract(frame, save=True, destination=None):

	## preprocess image from frame
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	cascade_xml = get_cascade()
	cascade = cv2.CascadeClassifier(cascade_xml)
	faces = cascade.detectMultiScale(frame, scaleFactor=1.5, minNeighbors=5)

	## check for destination directory
	final_dest = None
	if destination is not None:
		secondary = len(os.listdir(destination)) + 1
		final_dest = os.path.join(destination, f"Frame {secondary}")
		os.makedirs(final_dest, exist_ok=True)

	## bounding box coordinate checking
	paths = []
	for i, (x, y, w, h) in enumerate(faces):
		roi_color = frame[y:y+h, x:x+w]
		if save == True and destination != None:
			current_path = os.path.join(final_dest, f"{i}.jpg")
			cv2.imwrite(current_path, roi_color)
			paths.append(current_path)

	return paths
