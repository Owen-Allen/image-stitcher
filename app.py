import os
from flask import Flask, render_template, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
import datetime
from aws_utilities import lambda_get_request, upload_file, download_file

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.abspath('static/uploads')
app.config['RESULT_FOLDER'] = os.path.abspath('static/results')

LAMBDA_URL = "https://jp8nmjnyo0.execute-api.us-west-2.amazonaws.com/create-stitch/image-stitcher"
BUCKET_URL = "https://opencv-data.s3.us-east-2.amazonaws.com/"
BUCKET = "opencv-data"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == 'GET':
        # print("Whats good")
        return render_template('index.html')

@app.route("/result", methods=["GET", "POST"])
def result():
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
            left_image_path = os.path.join(app.config['UPLOAD_FOLDER'], left_image_filename)
            left_image.save(left_image_path)
            
            right_image_filename = secure_filename(right_image.filename)
            right_image_path = os.path.join(app.config['UPLOAD_FOLDER'], right_image_filename)
            right_image.save(right_image_path)


            # upload left and right file to s3 bucket
            res_left = upload_file(left_image_path, BUCKET)
            res_right = upload_file(right_image_path, BUCKET)

            if(not res_left or not res_right):
                print('error uploading files to s3')
                return

            # trigger lambda and get name of the result file

            result_filename = lambda_get_request(LAMBDA_URL, left_image_filename, right_image_filename)

            print(result_filename)
            if(result_filename == ""):
                print('error during lambda function execution')
                return

            # get result file from s3
            # result_image_fullpath = os.path.join(app.config['RESULT_FOLDER'], result_filename)
            # print(result_image_fullpath)
            # res_download = download_file(result_filename, BUCKET, result_image_fullpath)

            
            image_url = BUCKET_URL + result_filename
            print(image_url)
            return render_template('result.html', image_url=image_url)
        return render_template('index.html')





@app.route("/about", methods=["GET", "POST"])
def about():
    return render_template('about.html')


@app.route("/demo")
def demo():
    return render_template('demo.html')
