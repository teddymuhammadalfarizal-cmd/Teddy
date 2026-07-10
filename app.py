import streamlit as st

st.title("AI Face Swap Abi")
st.write("Wilujeng sumping di aplikasi AI buatan abi!")

user_input = st.text_input("Tulis nami anjeun:")
if user_input:
    st.write(f"Halo {user_input}, 
