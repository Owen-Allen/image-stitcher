# Image Stitcher

Flask web app that stitches images together using AKAZE local features matching, planar homography, image warping and other computer vision techniques.

CURRENT ISSUES:
- Vercel requests timeout after 10 seconds, and the lambda function takes longer than that to complete (for large inputs especially), stopping us from passing the result image url
- Solution: Have the Flask request server create the name of the result file and pass that name to the lambda function. Then complete the request and have the frontend wait/load the result once the lambda function is complete

<p float="left">
<img alt="Left image" src="https://github.com/Owen-Allen/image-stitcher/blob/main/static/left_art.png" width="400">
<img alt="Right image" src="https://github.com/Owen-Allen/image-stitcher/blob/main/static/right_art.png" width="400">
</p>

<img alt="Result image" src="https://github.com/Owen-Allen/image-stitcher/blob/main/static/ffa2daf6-a7e4-4fe3-a4ce-e445a2a0cc52.png" width="600">

### Program Flow: Lambda function

- Upload left and right image to s3 bucket
- http trigger lambda function, passing the name of the left and right image as parameters
- lambda function processes the images, saving to s3
- lambda function returns the name of the image in the s3 bucket
- flask app grabs the image from the s3 bucket


<img alt="Process diagram" src="https://github.com/Owen-Allen/image-stitcher/blob/main/static/diagram.jpg" width="800">


### Lambda & Api Gateway configuration

Get request requires 2 query params
left=left_file_name
right=right_file_name

Returns the name of the result file
