import uvicorn
from fastapi import FastAPI, File, UploadFile
from utils import load_image, load_model, predict
from starlette.responses import RedirectResponse

model_name = 'model_trained_2.p'
threshold = 0.85

description = """
<h2> Devel version 1 <h2>
"""

app = FastAPI(title='Digit Classification', description=description)

@app.get('/', tags=['Main Index'])
async def index():
	return RedirectResponse(url="/docs")

@app.post('/predict', tags=['Prediction'])
async def predict_image(file: UploadFile = File(...)):
	extension = file.filename.split(".")[-1] in ("jpg", "jpeg", "png")
	if not extension:
		return "Image must be jpg or png format!"

	# read the file object
	image = load_image(await file.read())

	# load model
	model = load_model(model_name)

	# predict the file
	result = predict(image, threshold, model)

	return result

# if __name__ == "__main__":
# 	uvicorn.run(app, port=8000, host='127.0.0.1', debug=True)