import streamlit as st
from PIL import Image

from pages import Nexrad

if __name__ == "__main__":
    st.title("Assignment 1 Team 07")
    image = Image.open('image.png')
    st.image(image, caption='four humans working on satelite data from the moon')