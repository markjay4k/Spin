from PIL import Image
from io import BytesIO
import requests


def add_border(image_url, thickness, color):
    response = requests.get(image_url)
    image = Image.open(BytesIO(response.content))
    bordered_image = Image.new(
        "RGB", (
            image.width + 2*thickness, 
            image.height + 2*thickness
        ), color
    )
    bordered_image.paste(image, (thickness, thickness))
    return bordered_image


def cover_bytes(movie, border=5, color='blue'):
    try:
        resp = requests.get(movie[b'full-size cover url'])
    except KeyError as e:
        return None, e
    else:
        image = Image.open(BytesIO(resp.content))
        image_border = Image.new(
            'RGB', (
                image.width + 2*border, image.height + 2*border,
            ), color
        )
        return image_border.paste(image, (border, border)), None
