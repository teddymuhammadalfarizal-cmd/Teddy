import streamlit as st
import replicate
import os

# Ngambil token tina Secrets
os.environ["REPLICATE_API_TOKEN"] = st.secrets["REPLICATE_API_TOKEN"]

st.title("AI Face Swap Abi")

uploaded_file = st.file_uploader("Upload foto anjeun...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    st.image(uploaded_file, caption='Foto nu di-upload', use_column_width=True)
    
    if st.button("Mulai Face Swap"):
        with st.spinner("Nuju ngaprosés AI... antosan sakedap!"):
            try:
                # Ngagunakeun model face swap
                output = replicate.run(
                    "lucataco/faceswap:9a4253335805561633d7d7f7813a86355606d289053592476579f1702f3a6135",
                    input={"target_image": uploaded_file}
                )
                st.image(output, caption='Hasil Face Swap')
            except Exception as e:
                st.error(f"Aya kasalahan: {e}")
