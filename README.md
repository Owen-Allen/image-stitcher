### Program Flow: Lambda function

- Upload left and right image to s3 bucket
- http trigger lambda function, passing the name of the left and right image as parameters
- lambda function processes the images, saving to s3
- lambda function returns the name of the image in the s3 bucket
- flask app grabs the image from the s3 bucket


### Lambda & Api Gateway configuration

Get request requires 2 query params
left=left_file_name
right=right_file_name

Returns the name of the result file