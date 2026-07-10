import streamlit as st
import requests

st.title("Image Generator (Gemini)")

deskripsi = st.text_area("Deskripsi gambar:", "Wanita muda sawo matang")

if st.button("Generate Image"):
    try:
        # Ambil API Key dari Secrets Streamlit milikmu
        api_key = st.secrets["GOOGLE_API_KEY"]
        
        with st.spinner("Nuju diproses, mangga antosan..."):
            # JALUR BARU: Menggunakan endpoint resmi khusus API Key dari Google AI Studio
            url = f"https://generativelanguage.googleapis.com/v1beta/models/imagen-3.0-generate-002:generateImages?key={api_key}"
            
            # Format data yang benar sesuai panduan Google AI Studio API
            payload = {
                "prompt": deskripsi,
                "numberOfImages": 1,
                "aspectRatio": "1:1",
                "outputMimeType": "image/jpeg"
            }
            
            # Kirim permintaan ke server Google
            response = requests.post(url, json=payload)
            response_data = response.json()
            
            # Cek apakah ada error dari server Google
            if response.status_code != 200:
                st.error(f"Error dari Google API: {response_data.get('error', {}).get('message', 'Unknown Error')}")
            else:
                # Mengambil data gambar imageBytes
                image_base64 = response_data['generatedImages'][0]['image']['imageBytes']
                
                # Menampilkan gambar langsung di web Streamlit
                st.image(f"data:image/jpeg;base64,{image_base64}", caption=deskripsi, use_container_width=True)
                
    except KeyError:
        st.error("Aya kalepatan: Pastikan di menu Secrets Streamlit sudah ditulis GOOGLE_API_KEY")
    except Exception as e:
        st.error(f"Aya kalepatan sistem: {e}")
