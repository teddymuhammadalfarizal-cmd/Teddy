import streamlit as st
from google import genai
import io
from PIL import Image

st.title("Image Generator (Gemini/Imagen)")

# Input API Key (bisa ditaruh di st.secrets atau input text)
api_key = st.text_input("Masukkan API Key Anda:", type="password")

deskripsi = st.text_area("Deskripsi gambar:", "Wanita muda sawo matang")

if st.button("Generate Image"):
    if not api_key:
        st.error("Cobi parios deui API Keyna (Mohon masukkan API Key terlebih dahulu).")
    else:
        try:
            # Menginisialisasi client dengan library google-genai yang baru
            client = genai.Client(api_key=api_key)
            
            with st.spinner("Nuju diproses, mangga antosan... (Sedang memproses...)"):
                # Memanggil model Imagen 3 untuk generate gambar
                result = client.models.generate_images(
                    model='imagen-3.0-generate-002',
                    prompt=deskripsi,
                )
                
                # Mengambil gambar dari hasil response
                for generated_image in result.generated_images:
                    image_bytes = generated_image.image.image_bytes
                    image = Image.open(io.BytesIO(image_bytes))
                    
                    # Menampilkan gambar di Streamlit
                    st.image(image, caption=deskripsi, use_container_width=True)
                    
        except Exception as e:
            st.error(f"Aya kalepatan: {e}")
