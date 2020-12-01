# Crop box
Tool for detecting bounding box and cropping picture to remove unecessary parts of an image. Could for example be used as an image transformation in a CNN.

## Example
Original picture of a cat in from `media/cat.jpg`
![Cat](https://github.com/haraldvinje/crop_box/blob/main/media/cat.jpg?raw=true)
`python crop_image_object.py media/cat.jpg` 

saves a new file in `out/cropped_cat.jpg`
![Cropped cat](https://github.com/haraldvinje/crop_box/blob/main/output/cropped_cat.jpg?raw=true)

## Disclaimer
This code uses the Python SDK for AWS and the AWS Rekognition service. To use this API, you'll need and AWS account and programmatic access keys. There is also a small fee for every API call, so use it cautiously.
