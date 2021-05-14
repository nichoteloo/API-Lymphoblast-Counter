import cv2
import pickle
from PIL import Image

def read_img(img):
	pil_image = Image.open(img)
	return pil_image

def preProcessing(img):
    img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    img = cv2.equalizeHist(img) # Makes the lighting of image distribute evenly
    img = img/255
    return img

def load_model(file):
	pickle_in = open(file,"rb")
	model = pickle.load(pickle_in)
	return model

def predict(img, threshold, model):
	resize_img = cv2.resize(img, (32,32))
	processed_img = preProcessing(resize_img)
	reshaped_img = processed_img.reshape(1,32,32,1)
	predictions = model.predict(reshaped_img) 
   	probVal = np.amax(predictions)
   	
    if (probVal > threshold):
    	return classIndex
	return "Hmm, not pretty sure"