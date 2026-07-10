import streamlit as st
import replicate
import os

# Konfigurasi Token
os.environ["REPLICATE_API_TOKEN"] = st.secrets["REPLICATE_API_TOKEN"]

st.set_page_config(page_title="AI Prompt Builder", layout="centered")
st.title("✨ AI Prompt Builder Abi")

# 1. Pose Selection
pose = st.selectbox("Pose Selection:", ["Custom Pose", "Standing", "Sitting", "Action Shot", "Close-up Portrait"])

# 2. Aspect Ratio
ratio = st.selectbox("Aspect Ratio:", ["9:16 (UGC Portrait)", "1:1 (Square)", "16:9 (Landscape)"])

# 3. Scene Description
description = st.text_area("Describe the scene:", placeholder="Contona: Wanita keur di taman, baju kasual, gaya candid...")

# 4. Camera Style & Lighting
camera = st.selectbox("Camera Style:", ["iPhone UGC", "DSLR", "Cinematic", "Vintage Film"])
lighting = st.selectbox("Lighting:", ["Golden Hour", "Studio Light", "Natural Light", "Neon"])

if st.button("Generate Image"):
    if not description:
        st.warning("Mangga eusian heula deskripsi adeganna!")
    else:
        with st.spinner("Nuju ngagambar ku AI... antosan sakedap!"):
            # Ngahiji-keun sadaya input jadi hiji prompt anu sae
            full_prompt = f"{description}, {pose}, {camera} style, {lighting} lighting, high quality, 4k"
            
            try:
                # Ngagunakeun model Flux anu realistis
                output = replicate.run(
                    "black-forest-labs/flux-schnell",
                    input={
                        "prompt": full_prompt,
                        "aspect_ratio": ratio.split(" ")[0]
                    }
                )
                st.image(output[0], caption="Hasil Generasi AI")
            except Exception as e:
                st.error(f"Aya kasalahan: {e}")
