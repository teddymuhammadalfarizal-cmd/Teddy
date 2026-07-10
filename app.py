import streamlit as st
import replicate
import os

# Ngambil token tina Secrets
os.environ["REPLICATE_API_TOKEN"] = st.secrets["REPLICATE_API_TOKEN"]

st.title("AI Face Swap Abi")

uploaded_file = st.file_uploader("Upload foto anjeun...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    st.image(uploaded_file, caption='Foto nu di-upload', use_column_width=True)
    
    # Nanya target gambar (beungeut nu rék dipasang)
    target_file = st.file_uploader("Upload foto target (beungeut nu rék ditiru)...", type=["jpg", "jpeg", "png"])
    
    if target_file is not None and st.button("Mulai Face Swap"):
        with st.spinner("Nuju ngaprosés AI... antosan sakedap!"):
            try:
                # Ngagunakeun model InsightFace anu leuwih stabil
                output = replicate.run(
                    "deep-floyd/if:a2a6eb43e12918844510006323145624790807530419355745404d5389600a0e",
                    input={
                        "prompt": "face swap",
                        "input_image": uploaded_file,
                        "target_image": target_file
                    }
                )
                st.image(output, caption='Hasil Face Swap')
            except Exception as e:
                st.error(f"Aya kasalahan: {e}")
