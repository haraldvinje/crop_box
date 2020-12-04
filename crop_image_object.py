from lib.aws_rekognition.rekognition_image_detection import get_bounding_box_of_object, get_bounding_box_of_numpy_image
from PIL import Image
from pathlib import Path
import uuid
from sys import argv
import cv2
import numpy as np


def get_picture_coordinates(bounding_box, image):
    if isinstance(image, str):
        input_image = Image.open(image)
        image_width, image_height = input_image.size
    elif isinstance(image, np.ndarray):
        input_image = image
        image_height = input_image.shape[0]
        image_width = input_image.shape[1]
    else:
        input_image = image
        image_width, image_height = input_image.size

    left = bounding_box['Left']
    top = bounding_box['Top']
    height = bounding_box['Height']
    width = bounding_box['Width']

    x0 = image_width*left
    y0 = image_height*top
    x1 = x0 + image_width*width
    y1 = y0 + image_height*height

    return x0, y0, x1, y1


def crop_image(image, x0, y0, x1, y1):
    if isinstance(image, str):
        return Image.open(image).crop((x0, y0, x1, y1))
    elif isinstance(image, np.ndarray):
        x0, y0, x1, y1 = int(x0), int(y0), int(x1), int(y1)
        return image[y0:(y1+1), x0:(x1+1)]
    else:
        try:
            return image.crop((x0, y0, x1, y1))
        except:
            raise Exception(
                "Unknown picture format. Accepts PIL or Numpy arrays")


def crop_numpy_image_to_bounding_box(numpy_image):
    try:
        bounding_box = get_bounding_box_of_numpy_image(numpy_image)
        x0, y0, x1, y1 = get_picture_coordinates(bounding_box, numpy_image)
        return crop_image(numpy_image, x0, y0, x1, y1)
    except:
        return numpy_image


def crop_PIL_image_to_bounding_box(filename):
    image = Image.open(filename)
    try:
        bounding_box = get_bounding_box_of_object(image_file_name=filename)
        x0, y0, x1, y1 = get_picture_coordinates(bounding_box, image)
        return crop_image(image, x0, y0, x1, y1)
    except:
        return image


def save_PIL_to_file(PIL_image, filename):
    directory = "output"
    filepath, extension = filename.split('.')
    name = filepath.split("/")[-1]
    output_file = directory + "/" + name + "." + extension
    path = Path(directory)
    path.mkdir(parents=True, exist_ok=True)
    file_exists = Path(output_file)
    if file_exists.is_file():
        output_file = directory + "/" + name + \
            str(uuid.uuid4()) + "." + extension
    PIL_image.save(output_file)


if __name__ == '__main__':
    filename = argv[1]

    # Numpy example
    numpy_image = cv2.imread(filename)
    cropped_numpy = crop_numpy_image_to_bounding_box(numpy_image)

    # Image file example
    cropped_image = crop_PIL_image_to_bounding_box(filename)
    save_PIL_to_file(cropped_image, filename)
