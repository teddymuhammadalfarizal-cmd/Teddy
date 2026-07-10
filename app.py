import streamlit as st
from google import genai
from google.genai import types
from PIL import Image
import io

# ========================================================
# KSTOMISASI WARNA LATAR & TEKS (DARK GRAY & WHITE)
# ========================================================
st.markdown(
    """
    <style>
    .stApp {
        background-color: #2F3136; /* Warna Kulawu Poék / Dark Gray */
    }
    h1, h2, h3, p, span, label {
        color: #FFFFFF !important; /* Warna Téks Bodas */
    }
    .stSelectbox div div {
        background-color: #40444B !important;
        color: #FFFFFF !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 1. Inisialisasi Gemini Client
client = genai.Client()

# 2. Judul Utama Aplikasi
st.title("📸 Gemini Canvas - Teddy Pro Edition")
st.write("Wilujeng sumping, Kang Teddy! Hayu urang ngadamel foto nu purna pas. ✨")

# 3. Kotak Tempat Upload Gambar (Layout Kolom)
col1, col2 = st.columns(2)

with col1:
    st.subheader("🖼️ Gambar Mentahan")
    img_base_file = st.file_uploader("Upload foto lokasi/objek asli", type=["jpg", "png", "jpeg"])
    # Pintonan langsung saatos di-upload
    if img_base_file:
        image_base_preview = Image.open(img_base_file)
        st.image(image_base_preview, caption="Preview Mentahan", use_container_width=True)

with col2:
    st.subheader("🤹 Gambar Referensi")
    img_ref_file = st.file_uploader("Upload foto karakter/pose", type=["jpg", "png", "jpeg"])
    # Pintonan langsung saatos di-upload
    if img_ref_file:
        image_ref_preview = Image.open(img_ref_file)
        st.image(image_ref_preview, caption="Preview Referensi", use_container_width=True)

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
            # 1️⃣ PROSES GEMINI
            with st.spinner("1️⃣ Gemini nuju nganalisa gambar & nyusun prompt... 🧠"):
                image_base = Image.open(img_base_file)
                image_ref = Image.open(img_ref_file)
                
                camera_instruction = "shot on iPhone 15 Pro Max, mobile photography, HDR" if gaya_kamera == "iPhone 15 Pro Max HDR+" else "professional DSLR photography, 85mm lens"
                blur_instruction = "shallow depth of field, creamy bokeh" if fokus_latar == "Bokeh blur" else "sharp focus, deep depth of field"
                
                main_prompt = f"""
                Create a detailed image prompt blending these two. Place the subject from Image 2 inside the environment of Image 1.
                Strictly apply: {jumlah_orang}, {camera_instruction}, {blur_instruction}. Output prompt ONLY.
                """
                
                response = client.models.generate_content(
                    model='gemini-2.0-flash',
                    contents=[image_base, image_ref, main_prompt]
                )
                compiled_prompt = response.text

            with st.expander("📝 Tingal Prompt Hasil Racikan Gemini"):
                st.text_area("Compiled Prompt:", compiled_prompt, height=100)

            # 2️⃣ PROSES IMAGEN 3
            with st.spinner("2️⃣ Imagen 3 nuju ngadamel gambar anyar Akang... 🎨"):
                imagen_aspect_ratio = "1:1"
                if "16:9" in rasio_gambar:
                    imagen_aspect_ratio = "16:9"
                elif "4:3" in rasio_gambar:
                    imagen_aspect_ratio = "4:3"
                
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
                
                for generated_image in imagen_response.generated_images:
                    image_bytes = io.BytesIO(generated_image.image.image_bytes)
                    final_image = Image.open(image_bytes)
                    
                    st.subheader("✨ Hasil Gambar Anyar:")
                    st.image(final_image, caption=f"Hasil requested ku Kang Teddy ({rasio_gambar})", use_container_width=True)
                    
                    # 🎈 EFEK ANIMASI BALON UPAMI SUKSES
                    st.balloons()
                    st.success("Hore! Gambar parantos ngawujud, mang! 🎉")
                    
        except Exception as e:
            st.error(f"Aya masalah téknis, mang: {e}")
    else:
        st.warning("Punten lebetkeun Gambar Mentahan sareng Gambar Referensi heula nya, Kang Teddy! ⚠️")
