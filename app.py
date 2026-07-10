import streamlit as st
import google.generativeai as genai

# Konfigurasi API Key
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

st.title("✨ AI Image Generator (Gemini)")

# Input Deskripsi
prompt = st.text_area("Deskripsi gambar:", placeholder="Contona: Wanita keur di taman, gaya candid...")

if st.button("Generate Image"):
    if prompt:
        with st.spinner("Nuju ngagambar ku Gemini... antosan sakedap!"):
            try:
                # Ngagunakeun Imagen 3 pikeun ngahasilkeun gambar
                result = genai.generate_images(
                    prompt=prompt,
                    number_of_images=1,
                    output_mime_type="image/jpeg"
                )
                
                # Nampilkeun gambar dina Streamlit
                for image in result.generated_images:
                    st.image(image.image.image_bytes, caption="Hasilna!")
                    
            except Exception as e:
                st.error(f"Aya kasalahan: {e}")
                st.write("Cobi parios deui API Key atanapi sambungan internetna.")
    else:
        st.warning("Mangga eusian heula deskripsi gambarna!")
