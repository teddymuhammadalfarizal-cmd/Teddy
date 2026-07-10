import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

# Konfigurasi Gemini
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel('imagen-3.0-generate-001')

st.title("✨ AI Image Generator (Gemini)")

prompt = st.text_area("Deskripsi gambar:")

if st.button("Generate Image"):
    if prompt:
        with st.spinner("Nuju ngagambar ku Gemini..."):
            try:
                result = model.generate_images(prompt=prompt)
                for image in result.generated_images:
                    img = Image.open(io.BytesIO(image.image.image_bytes))
                    st.image(img, caption="Hasilna!")
            except Exception as e:
                st.error(f"Aya kasalahan: {e}")
