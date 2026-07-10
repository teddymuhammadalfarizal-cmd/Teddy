import streamlit as st
import requests

st.title("Image Generator (Gemini)")

deskripsi = st.text_area("Deskripsi gambar:", "Wanita muda sawo matang")

if st.button("Generate Image"):
    try:
        # 1. Ambil API Key dari Secrets Streamlit milikmu
        api_key = st.secrets["GOOGLE_API_KEY"]
        
        with st.spinner("Nuju diproses, mangga antosan..."):
            # 2. Setup URL API resmi Google Imagen 3
            url = f"https://generativelanguage.googleapis.com/v1beta/models/imagen-3.0-generate-002:predict?key={api_key}"
            
            # 3. Setup data format yang diminta oleh Google API
            payload = {
                "instances": [
                    {
                        "prompt": deskripsi
                    }
                ],
                "parameters": {
                    "sampleCount": 1,
                    "aspectRatio": "1:1",
                    "outputMimeType": "image/jpeg"
                }
            }
            
            # 4. Kirim permintaan ke server Google
            response = requests.post(url, json=payload)
            response_data = response.json()
            
            # 5. Cek apakah ada error dari server Google
            if response.status_code != 200:
                st.error(f"Error dari Google API: {response_data.get('error', {}).get('message', 'Unknown Error')}")
            else:
                # 6. Mengambil gambar berbasis Base64 dari hasil response
                image_base64 = response_data['predictions'][0]['bytesBase64Encoded']
                
                # 7. Menampilkan gambar langsung di web Streamlit
                st.image(f"data:image/jpeg;base64,{image_base64}", caption=deskripsi, use_container_width=True)
                
    except KeyError:
        st.error("Aya kalepatan: Pastikan di menu Secrets Streamlit sudah ditulis GOOGLE_API_KEY")
    except Exception as e:
        st.error(f"Aya kalepatan sistem: {e}")
