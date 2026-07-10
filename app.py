import streamlit as st
import google.generativeai as genai

st.title("Image Generator (Gemini)")

# Kolom deskripsi langsung di atas tanpa input API Key lagi
deskripsi = st.text_area("Deskripsi gambar:", "Wanita muda sawo matang")

if st.button("Generate Image"):
    try:
        # Mengambil API Key secara otomatis dari Secrets Streamlit
        api_key = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=api_key)
        
        with st.spinner("Nuju diproses..."):
            # Memanggil model Imagen 3
            model = genai.ImageGenerationModel("imagen-3.0-generate-002")
            result = model.generate_images(
                prompt=deskripsi,
                number_of_images=1,
                aspect_ratio="1:1"
            )
            
            # Menampilkan hasil gambar
            for image in result.images:
                st.image(image.image, caption=deskripsi)
                
    except KeyError:
        st.error("Aya kalepatan: GEMINI_API_KEY belum disetting di Secrets Streamlit Cloud.")
    except Exception as e:
        st.error(f"Aya kalepatan: {e}")
