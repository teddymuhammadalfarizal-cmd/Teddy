import streamlit as st
from PIL import Image

st.title("AI Face Swap Abi")
st.write("Upload foto anjeun di dieu:")

uploaded_file = st.file_uploader("Pilih gambar...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Foto nu di-upload')
    st.write("Gambar tos siap!")
