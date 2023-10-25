import requests
import json
import base64
import boto3
from botocore.exceptions import ClientError
import logging
import os


LAMBDA_URL = "https://jp8nmjnyo0.execute-api.us-west-2.amazonaws.com/create-stitch/image-stitcher"
BUCKET = "opencv-data"


def upload_file(file_name, bucket, object_name=None):
    # https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-uploading-files.html
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        print('error uploading')
        print(e)
        return False
    return True


def download_file(file_name, bucket, save_path=None):
    try:
        s3 = boto3.resource('s3')
        if(save_path == None):
            s3.meta.client.download_file(bucket, file_name, file_name)
        else:
            s3.meta.client.download_file(bucket, file_name, save_path)
        return True
    except Exception as e:
        print('error downloading')
        print(e)
        return False


def lambda_get_request(function_url, left_filename, right_filename):
    query_params = f'?left={left_filename}&right={right_filename}'
    full_url = function_url + query_params
    print(full_url)
    r = requests.get(full_url)
    print(r)
    print(r.status_code)
    print(r.content)
    if r.status_code == 200:
        response_data = r.content
        response_string = response_data.decode('utf-8')
        response_dict = json.loads(response_string)
        result_filename = response_dict['result_filename']
        return result_filename
    return ''


def stitch_process(left_image_filename, right_image_filename, bucket):
    upload_res_left = upload_file(left_image_filename, bucket)
    upload_res_right = upload_file(right_image_filename, bucket)
    if(not upload_res_left or not upload_res_right):
        print(f'upload_res_left {upload_res_left}')
        print(f'upload_res_right {upload_res_right}')
        return 'error uploading images'
    
    print('finished uploading images')
    
    result_filename = lambda_get_request(LAMBDA_URL, left_image_filename, right_image_filename)

    if(not result_filename):
        return 'error running lambda'
    
    print(result_filename)
    download_res = download_file(result_filename, bucket)

    if(not download_res):
        return 'error downloading image'

    return True


if __name__=='__main__':
    # test_connection()
    # test_upload()
    # download_file('grayscale.png', BUCKET)
    # print(stitch_process('left_art.png', 'right_art.png', BUCKET))
    # run_lambda()
    print()