import streamlit as st
import requests
from PIL import Image
from io import BytesIO


FASTAPI_SERVER_URL = "http://192.168.10.67:8000"


def get_image_from_fastapi():
    response = requests.get(f"{FASTAPI_SERVER_URL}/image")
    if response.status_code == 200:
        return Image.open(BytesIO(response.content))
    return None


def main():
    st.title("Clickable Image with FastAPI and Streamlit")
    image = get_image_from_fastapi()
    if image:
        if st.image(
            image, use_column_width=True,
            caption="Click me!", output_format='JPEG'
        ):
            st.write("Image clicked!")
    else:
        st.error("Failed to load the image from FastAPI server.")

if __name__ == "__main__":
    main()

