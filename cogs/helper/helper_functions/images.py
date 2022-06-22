# *********************************************************************************************************************
# images.py
# import cogs.helper.helper_functions.images as images
# *********************************************************************************************************************

import os
import requests
from io import BytesIO

from PIL import Image

# get current directory
current_directory = os.path.dirname(os.path.realpath(__file__))
images_directory = "/".join(list(current_directory.split('/')
                            [0:-3])) + '/resource_files/image_files/'


def get_image_path(file_name):
    return images_directory + file_name


def get_image_by_path(path):
    return Image.open(path)


def get_image_by_url(url):
    response = requests.get(url)
    return Image.open(BytesIO(response.content))


def save_image(image, path):
    image.save(path, "PNG")


def merge_images_width_wise(image1, image2, save_path, offset=0):
    image1_size = image1.size
    image2_size = image2.size
    new_image = Image.new(
        'RGB', (image1_size[0]+image2_size[0], image1_size[1] + offset), (0, 0, 0))
    new_image.paste(image1, (0, offset))
    new_image.paste(image2, (image1_size[0], 0))
    new_image.save(save_path, "PNG")


def delete_image(path):
    if os.path.isfile(path):
        os.remove(path)
