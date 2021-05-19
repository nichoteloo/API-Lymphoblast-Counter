import requests
from threading import Thread
from flask import Flask, redirect, render_template, request, flash

app = Flask(__name__)
app.secret_key = b'/R\x99.\xda\xba\x9dD\\.C)f4\x19\x1b\x8b\xa7\x12\xd7\x07\xed\x13\x90'

@app.route('/test')
def home():
    return render_template('index.html')

def send_image_req(url,data):
    my_img = {'file': open(data, 'rb')}
    response = requests.post(url, files=my_img)
    return response.json()

@app.route('/test',methods=['POST'])
def load_image():
    url = 'http://127.0.0.1:5000/api/upload'

    if request.method == 'POST':
        file = request.files.get('file')
        data = file.filename
        response = send_image_req(url,data)
        saved = response['saved']
        # import pdb; pdb.set_trace()
        if saved:
            flash('Yey image successfully uploaded')
        else:    
            flash('Nothing happens so far')
            return render_template("index.html",)
    
    return render_template("index.html", message="Your request is not reached")


@app.route('/', methods=['POST'])
def display_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']

    img = Image.open(file.stream)

    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
    	filename = secure_filename(file.filename)
    	file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename)) ## saving file
        #print('upload_image filename: ' + filename)
    	flash('Image successfully uploaded and displayed below')
    	return render_template('index.html', filename=filename)
    else:
        flash('Allowed image types are - png, jpg, jpeg, gif')
        return redirect(request.url)

# @app.route('/display/<filename>')
# def display_image(filename):
#     return redirect(url_for('static', filename='uploads/' + filename), code=301)

if __name__ == "__main__":
    app.run(port=5001, debug=True)