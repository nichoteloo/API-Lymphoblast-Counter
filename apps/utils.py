import cv2
import pickle
import numpy as np
from PIL import Image

def load_image(data):
	'''
	input: image from file object
	output: array-like image 3 channel (128,128,3)
	'''
	npimg = np.frombuffer(data, np.uint8)
	frame = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
	return frame

def preProcessing(img):
	'''
	input: array-like image
	output: precolorize image
	'''
	img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	img = cv2.equalizeHist(img) # makes the lighting of image distribute evenly
	return img/255

def load_model(model_file):
	'''
	input: path for model
	output: instance of model
	'''
	pickle_in = open(model_file,"rb")
	model = pickle.load(pickle_in)
	return model

def predict(img, threshold, model):
	'''
	input: raw image, acc threshold number, instance model
	output: class index
	'''
	img_array = np.asarray(img)
	resize_img = cv2.resize(img_array, (32,32))
	processed_img = preProcessing(resize_img)
	reshaped_img = processed_img.reshape(1,32,32,1)

	classIndex = model.predict_classes(reshaped_img)
	predictions = model.predict(reshaped_img) 
	probVal = np.amax(predictions)
   	
   	# thesholding for accuracy
	if (probVal > threshold):
		return classIndex
	return "Hmm, not pretty sure"