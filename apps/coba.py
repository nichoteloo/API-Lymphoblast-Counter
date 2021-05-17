from fastapi import FastAPI, UploadFile, File, Form
from PIL import Image
from io import BytesIO
import numpy as np
import cv2

app = FastAPI()

def load_image(data):
	npimg = np.frombuffer(data, np.uint8)
	frame = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
	return frame

@app.post("/")
async def read_root(file: UploadFile = File(...)):
    # image = load_image_into_numpy_array(await file.read())
    # image = cv2.imread(image)
    # print(image.shape)
    # print(type(image))
    image = load_image(await file.read())
    print(image.shape)
    return {"Hello": "World"}