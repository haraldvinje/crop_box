from lib.aws_rekognition.rekognition_image_detection import get_bouding_box_of_object
from PIL import Image
from pathlib import Path
import uuid
from sys import argv


def crop_PIL_image_to_bounding_box(filename):
    image = Image.open(filename)

    bounding_box = get_bouding_box_of_object(image_file_name=filename)
    left = bounding_box['Left']
    top = bounding_box['Top']
    height = bounding_box['Height']
    width = bounding_box['Width']

    image_width, image_height = image.size

    x0 = image_width*left
    y0 = image_height*top
    x1 = x0 + image_width*width
    y1 = y0 + image_height*height

    cropped = image.crop((x0, y0, x1, y1))
    return cropped


def save_PIL_to_file(PIL_image, filename):
    directory = "output"
    filepath, extension = filename.split('.')
    name = filepath.split("/")[-1]
    output_file = directory + "/" + name + "." + extension
    path = Path(directory)
    path.mkdir(parents=True, exist_ok=True)
    file_exists = Path(output_file)
    if file_exists.is_file():
        output_file = directory + "/" + name + str(uuid.uuid4()) + "." + extension
    PIL_image.save(output_file)

if __name__=='__main__':
    filename = argv[1]
    cropped_image = crop_PIL_image_to_bounding_box(filename)
    save_PIL_to_file(cropped_image, filename)