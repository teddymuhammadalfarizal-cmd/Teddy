import streamlit as st
import replicate
import os

os.environ["REPLICATE_API_TOKEN"] = st.secrets["REPLICATE_API_TOKEN"]

st.title("AI Prompt Builder Abi")

# Input kanggo Deskripsi / Prompt
prompt = st.text_area("Describe the scene (Deskripsi adegan):", placeholder="Contona: Wanita keur di taman, baju kasual...")
aspect_ratio = st.selectbox("Aspect Ratio:", ["9:16", "1:1", "16:9"])

if st.button("Generate Image"):
    with st.spinner("Nuju ngagambar ku AI..."):
        try:
            # Ngagunakeun model Flux (nuju populer tur realistis)
            output = replicate.run(
                "black-forest-labs/flux-schnell",
                input={
                    "prompt": prompt,
                    "aspect_ratio": aspect_ratio
                }
            )
            st.image(output[0], caption="Hasilna!")
        except Exception as e:
            st.error(f"Aya kasalahan: {e}")
