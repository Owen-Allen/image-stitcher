# Image Stitcher


<p float="left">
<img alt="Left image" src="https://github.com/Owen-Allen/image-stitcher/blob/main/static/left_art.png" width="200">
<img alt="Right image" src="https://github.com/Owen-Allen/image-stitcher/blob/main/static/right_art.png" width="200">
</p>

<img alt="Result image" src="https://github.com/Owen-Allen/image-stitcher/blob/main/static/ffa2daf6-a7e4-4fe3-a4ce-e445a2a0cc52.png" width="400">

### Program Flow: Lambda function

- Upload left and right image to s3 bucket
- http trigger lambda function, passing the name of the left and right image as parameters
- lambda function processes the images, saving to s3
- lambda function returns the name of the image in the s3 bucket
- flask app grabs the image from the s3 bucket


<img alt="Process diagram" src="https://github.com/Owen-Allen/image-stitcher/blob/main/static/diagram.jpg" width="400">


### Lambda & Api Gateway configuration

Get request requires 2 query params
left=left_file_name
right=right_file_name

Returns the name of the result file
