from fastapi import FastAPI
from fastapi import UploadFile, File
from server import read_img, load_model, predict
from starlette.responses import RedirectResponse
import uvicorn

model_name = 'model_trained_2.p'
threshold = 0.65

app = FastAPI()

@app.get('/')
def index():
	return RedirectResponse(url="/docs")

@app.get('/hello')
def hello_world(name: str):
	return f"hello {name}!"

@app.post('/api/predict')
def predict_image(file: UploadFile = File(...)):
	# read the file uploaded by the user
	image = read_img(File)

	# load model
	model = load_model(model_name)

	# after doing preprocessing
	img = np.asarray(image)

	# predict the file
	result = predict(img, threshold, model)

	return result

if __name__ == "__main__":
	uvicorn.run(app, port=8000, host='127.0.0.1', debug=True)