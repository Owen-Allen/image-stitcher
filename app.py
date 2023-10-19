import os
from flask import Flask, render_template, flash, request, redirect, url_for
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/uploads'

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == 'GET':
        print("Whats good")

        return render_template('index.html')
    if request.method == 'POST':
        print("RECIEVED POST REQUEST")
        print(request.files)
        if 'left_image' not in request.files or 'right_image' not in request.files:
            print("Missing files")
            return redirect(request.url)

        left_image = request.files['left_image']
        right_image = request.files['right_image']

        if left_image.filename == '' or right_image.filename == '':
            print('no images uploaded')
            return redirect(request.url)

        if left_image and allowed_file(left_image.filename) and right_image and allowed_file(right_image.filename):
            left_image_filename = secure_filename(left_image.filename)
            left_image.save(os.path.join(app.config['UPLOAD_FOLDER'], left_image_filename))

            right_image_filename = secure_filename(right_image.filename)
            right_image.save(os.path.join(app.config['UPLOAD_FOLDER'], right_image_filename))
            
                        
            return redirect(request.url)

        return render_template('index.html', result="result")


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    print("ayo we made it")
    if request.method == 'POST':
        print(request.files)
        # file.save(f"/var/www/uploads/{secure_filename(file.filename)}")