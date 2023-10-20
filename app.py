import os
from flask import Flask, render_template, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from stitch import stitch, hello_flask
import cv2 as cv


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.abspath('static/uploads')
app.config['RESULT_FOLDER'] = os.path.abspath('static/results')  # Set the absolute path for the results


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == 'GET':
        # print("Whats good")
        print(hello_flask())
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

            # totally could just use a stream, but for now this feels easier

            img1 = cv.imread(os.path.join(app.config['UPLOAD_FOLDER'], left_image_filename), 1)
            img2 = cv.imread(os.path.join(app.config['UPLOAD_FOLDER'], right_image_filename), 1)
            
            result_img = stitch(img2, img1)

            h, w, c = result_img.shape
            result_img_filename =  os.path.join(app.config['RESULT_FOLDER'],'result.png')
            cv.imwrite(result_img_filename, result_img)
            print(result_img_filename)
            return  render_template('result.html', result_image='static/results/result.png', height=h, width=w) # render_template('result.html', result_image="/uploads" + left_image_filename)
        return render_template('index.html')




@app.route("/about", methods=["GET", "POST"])
def about():
    return render_template('about.html')


@app.route("/demo")
def demo():
    return render_template('demo.html')
