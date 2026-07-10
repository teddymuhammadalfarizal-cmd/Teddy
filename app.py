import streamlit as st
from google import genai
from google.genai import types
from PIL import Image
import io

# 1. Inisialisasi Gemini Client
# SDK bakal otomatis milari GOOGLE_API_KEY atanapi GEMINI_API_KEY dina Streamlit Secrets / Env
client = genai.Client()

# 2. Judul Utama Aplikasi
st.title("📸 Gemini Canvas - Teddy Pro Edition")
st.write("Wilujeng sumping, Kang Teddy! Hayu urang ngadamel foto nu purna pas. ✨")

# 3. Kotak Tempat Upload Gambar (Layout Kolom)
col1, col2 = st.columns(2)

with col1:
    st.subheader("🖼️ Gambar Mentahan")
    img_base_file = st.file_uploader("Upload foto lokasi/objek asli", type=["jpg", "png", "jpeg"])

with col2:
    st.subheader("🤹 Gambar Referensi")
    img_ref_file = st.file_uploader("Upload foto karakter/pose", type=["jpg", "png", "jpeg"])

st.write("---")

# 4. Menu Pilihan Konfigurasi (Dropdown)
st.subheader("🎛️ Core Prompt Configurator")

col3, col4 = st.columns(2)

with col3:
    jumlah_orang = st.selectbox("🧑‍🤝‍🧑 Jumlah Orang:", ["1 orang", "2 orang", "3+ orang"])
    gaya_kamera = st.selectbox("📸 Gaya Kamera / Efek:", ["iPhone 15 Pro Max HDR+", "Kamera DSLR"])

with col4:
    rasio_gambar = st.selectbox("📐 Rasio Gambar:", ["1:1 (Square)", "16:9 (Widescreen)", "4:3 (Standard)"])
    fokus_latar = st.selectbox("🔍 Fokus Latar (Blur):", ["Bokeh blur", "Zero blur"])

st.write("---")

# 5. Tombol Utama sareng Proses AI
if st.button("🚀 GENERATE IMAGE", use_container_width=True):
    if img_base_file and img_ref_file:
        try:
            # Peta pondok kanggo spinner
            with st.spinner("1️⃣ Gemini 2.5 nuju nganalisa gambar & nyusun prompt... 🧠"):
                # Buka gambar nganggo PIL
                image_base = Image.open(img_base_file)
                image_ref = Image.open(img_ref_file)
                
                # Konversi pilihan dropdown janten instruksi basa Inggris
                camera_instruction = ""
                if gaya_kamera == "iPhone 15 Pro Max HDR+":
                    camera_instruction = "shot on iPhone 15 Pro Max, mobile photography, high dynamic range, vibrant colors, sharp details"
                elif gaya_kamera == "Kamera DSLR":
                    camera_instruction = "professional DSLR photography, shot on 85mm lens, sharp focus on subject, cinematic lighting, masterfully composed"
                    
                blur_instruction = "shallow depth of field, creamy bokeh background" if fokus_latar == "Bokeh blur" else "sharp focus, deep depth of field, clear background details"
                
                # Prompt utama pikeun Gemini 2.5 Flash
                main_prompt = f"""
                You are an expert image prompt generator. Analyze these two images:
                - Image 1 is the Base Image / Location / Environment.
                - Image 2 is the Reference Subject / Pose.
                
                Create a highly detailed, single-paragraph English image generation prompt that blends them perfectly.
                The final prompt must place the subject(s) from Image 2 into the exact environment of Image 1.
                
                Apply these specific user configurations strictly:
                - Number of people to depict: {jumlah_orang}
                - Photographic Style: {camera_instruction}
                - Background Focus: {blur_instruction}
                
                Output ONLY the final detailed prompt in English, do not add any conversational filler.
                """
                
                # Kirim ka Gemini 2.5 Flash
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=[image_base, image_ref, main_prompt]
                )
                compiled_prompt = response.text

            # Tembongkeun hasil prompt bilih hoyong dikoreksi
            with st.expander("📝 Tingal Prompt Hasil Racikan Gemini"):
                st.text_area("Compiled Prompt:", compiled_prompt, height=100)

            with st.spinner("2️⃣ Imagen 3 nuju ngadamel gambar anyar Akang... 🎨"):
                # Konversi rasio gambar
                imagen_aspect_ratio = "1:1"
                if "16:9" in rasio_gambar:
                    imagen_aspect_ratio = "16:9"
                elif "4:3" in rasio_gambar:
                    imagen_aspect_ratio = "4:3"
                
                # Kirim prompt ka Imagen 3
                imagen_response = client.models.generate_images(
                    model='imagen-3.0-generate-002',
                    prompt=compiled_prompt,
                    config=types.GenerateImagesConfig(
                        number_of_images=1,
                        output_mime_type="image/jpeg",
                        aspect_ratio=imagen_aspect_ratio,
                        person_generation="ALLOW_ADULT",
                    )
                )
                
                # Tembongkeun hasil gambar
                for generated_image in imagen_response.generated_images:
                    image_bytes = io.BytesIO(generated_image.image.image_bytes)
                    final_image = Image.open(image_bytes)
                    
                    st.subheader("✨ Hasil Gambar Anyar:")
                    st.image(final_image, caption=f"Hasil requested ku Kang Teddy ({rasio_gambar})", use_container_width=True)
                    st.success("Hore! Gambar parantos ngawujud, mang! 🎉")
                    
        except Exception as e:
            st.error(f"Aya masalah téknis, mang: {e}")
    else:
        st.warning("Punten lebetkeun Gambar Mentahan sareng Gambar Referensi heula nya, Kang Teddy! ⚠️")
