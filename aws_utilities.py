import requests
import json
import boto3
from botocore.config import Config
from botocore.exceptions import ClientError
import logging
import os

LAMBDA_URL = os.environ.get('LAMBDA_URL')
BUCKET_NAME = os.environ.get('BUCKET_NAME')
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')

def create_presigned_post(bucket_name, object_name,
                          fields=None, conditions=None, expiration=3600):
    """Generate a presigned URL S3 POST request to upload a file

    :param bucket_name: string
    :param object_name: string
    :param fields: Dictionary of prefilled form fields
    :param conditions: List of conditions to include in the policy
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Dictionary with the following keys:
        url: URL to post to
        fields: Dictionary of form fields and values to submit with the POST
    :return: None if error.
    """

    # Generate a presigned S3 POST URL
    s3_client = boto3.client("s3",
                             aws_access_key_id=AWS_ACCESS_KEY_ID, 
                             aws_secret_access_key=AWS_SECRET_ACCESS_KEY, 
                             )    
    try:
        response = s3_client.generate_presigned_post(bucket_name,
                                                     object_name,
                                                     Fields=fields,
                                                     Conditions=conditions,
                                                     ExpiresIn=expiration)
    except ClientError as e:
        logging.error(e)
        return None

    # The response contains the presigned URL and required fields
    return response

def upload_file(file_name, bucket_name, object_name=None):
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
    s3_client = boto3.client("s3",
                             aws_access_key_id=AWS_ACCESS_KEY_ID, 
                             aws_secret_access_key=AWS_SECRET_ACCESS_KEY, 
                             )
    try:
        response = s3_client.upload_file(file_name, bucket_name, object_name)
    except ClientError as e:
        print("error uploading")
        print(e)
        return False
    return True


def download_file(file_name, bucket_name, save_path=None):
    try:
        s3 = boto3.resource("s3")
        if save_path == None:
            s3.meta.client.download_file(bucket_name, file_name, file_name)
        else:
            s3.meta.client.download_file(bucket_name, file_name, save_path)
        return True
    except Exception as e:
        print("error downloading")
        print(e)
        return False


def lambda_get_request(function_url, left_filename, right_filename):
    query_params = f"?left={left_filename}&right={right_filename}"
    full_url = function_url + query_params
    print(full_url)
    r = requests.get(full_url)
    print(r)
    print(r.status_code)
    print(r.content)
    if r.status_code == 200:
        response_data = r.content
        response_string = response_data.decode("utf-8")
        response_dict = json.loads(response_string)
        result_filename = response_dict["result_filename"]
        return result_filename
    return ""


def stitch_process(left_image_filename, right_image_filename, bucket_name):
    upload_res_left = upload_file(left_image_filename, bucket_name)
    upload_res_right = upload_file(right_image_filename, bucket_name)
    if not upload_res_left or not upload_res_right:
        print(f"upload_res_left {upload_res_left}")
        print(f"upload_res_right {upload_res_right}")
        return "error uploading images"

    print("finished uploading images")

    result_filename = lambda_get_request(
        LAMBDA_URL, left_image_filename, right_image_filename
    )

    if not result_filename:
        return "error running lambda"

    print(result_filename)
    download_res = download_file(result_filename, bucket_name)

    if not download_res:
        return "error downloading image"

    return True


if __name__ == "__main__":
    # test_connection()
    # test_upload()
    # download_file('grayscale.png', BUCKET)
    # print(stitch_process('left_art.png', 'right_art.png', BUCKET))
    # run_lambda()
    print()
