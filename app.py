import os
from flask import Flask, render_template, flash, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
import datetime
from aws_utilities import lambda_get_request, upload_file, download_file, create_presigned_post
import logging

# from dotenv import load_dotenv
# load_dotenv()


app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = os.path.abspath("static/uploads")
app.config["RESULT_FOLDER"] = os.path.abspath("static/results")
logging.basicConfig(level=logging.INFO)

LAMBDA_URL = os.environ.get('LAMBDA_URL')
BUCKET_URL = os.environ.get('BUCKET_URL')
BUCKET_NAME = os.environ.get('BUCKET_NAME')


ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "GET":
        logging.info("GET /")

        return render_template("index.html")

@app.route('/result', methods=["POST"])
def result():
    print('IN RESULT')
    if request.method == "POST":
        print('here')
        if 'left' not in request.json or 'right' not in request.json:
            return 'Missing Parameters', 400
        
        print("here2")
        
        left_filename = request.json['left']
        right_filename = request.json['right']
        print("here 3")

        result_filename = lambda_get_request(LAMBDA_URL, left_filename, right_filename)

        if result_filename == "":
            app.logger.info("error during lambda function execution")
            return
        
        app.logger.info(f"Finished Lambda. result_filename: {result_filename}")

        image_url = BUCKET_URL + result_filename
        data = {'image_url': image_url}
        return data


        # get result file from s3
        # result_image_fullpath = os.path.join(app.config['RESULT_FOLDER'], result_filename)
        # logging.info(result_image_fullpath)
        # res_download = download_file(result_filename, BUCKET_NAME, result_image_fullpath)

@app.route("/about", methods=["GET", "POST"])
def about():
    return render_template("about.html")


@app.route("/demo")
def demo():
    return render_template("demo.html")

import requests
@app.route('/upload_url', methods=["POST"])
def upload_url():
    if request.method == "POST":
        req_data = request.get_json()
        file_name = req_data['file_name']
        # file_type = req_data['type']
        file_type = 'image/png'
        response = create_presigned_post(BUCKET_NAME, file_name)

        # with open('static/left_art_small.png', 'rb') as f:
        #     files = {'file': (file_name, f)}
        #     print(files)
        #     http_response = requests.post(response['url'], data=response['fields'], files=files)

        # logging.info(f'File upload HTTP status code: {http_response.status_code}')

        return response

    return  418, "its tea time"
    
