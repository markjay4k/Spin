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
