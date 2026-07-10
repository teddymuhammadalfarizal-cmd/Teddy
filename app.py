import streamlit as st
import google.generativeai as genai

st.title("Image Generator (Gemini)")

deskripsi = st.text_area("Deskripsi gambar:", "Wanita muda sawo matang")

if st.button("Generate Image"):
    try:
        # Membaca GOOGLE_API_KEY sesuai yang kamu tulis di menu Secrets
        api_key = st.secrets["GOOGLE_API_KEY"]
        genai.configure(api_key=api_key)
        
        with st.spinner("Nuju diproses..."):
            # Ini cara paling aman yang jalan di semua versi library google-generativeai
            response = genai.GenerativeModel("imagen-3.0-generate-002").generate_content(
                deskripsi
            )
            
            # Mengambil dan menampilkan gambar
            st.image(response.text, caption=deskripsi)
                
    except KeyError:
        st.error("Aya kalepatan: Pastikan nama di Secrets adalah GOOGLE_API_KEY")
    except Exception as e:
        st.error(f"Aya kalepatan: {e}")
