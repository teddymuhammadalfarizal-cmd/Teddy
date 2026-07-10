import streamlit as st
import requests
import io
from PIL import Image

st.title("Image Generator (Alternative)")

deskripsi = st.text_area("Deskripsi gambar:", "Wanita muda sawo matang")

if st.button("Generate Image"):
    if not deskripsi:
        st.error("Mangga serat heula deskripsi gambarna!")
    else:
        with st.spinner("Nuju diproses ku AI, mangga antosan..."):
            try:
                # Menggunakan API gratis tanpa key dari Pollinations AI (Server Hugging Face/Stable Diffusion)
                url = f"https://image.pollinations.ai/p/{requests.utils.quote(deskripsi)}?width=1024&height=1024&nologo=true"
                
                response = requests.get(url, timeout=30)
                
                if response.status_code == 200:
                    # Mengubah hasil response langsung menjadi gambar
                    image = Image.open(io.BytesIO(response.content))
                    
                    # Menampilkan gambar di web Streamlit
                    st.image(image, caption=deskripsi, use_container_width=True)
                else:
                    st.error("Server penc pembuat gambar sedang sibuk, cobi sakedap deui.")
                    
            except Exception as e:
                st.error(f"Aya kalepatan sistem: {e}")
