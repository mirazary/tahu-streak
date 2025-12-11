import streamlit as st
import os

def display_logo_center():
    logo_path = os.path.join("assets", "logo", "tahu_logo.png")

    col1, col2, col3 = st.columns([1, 0.5, 1])
    with col2:
        if os.path.exists(logo_path):
            st.image(logo_path, width=300)
        else:
            st.markdown("<h1 style='text-align:center;'>🔥 TAHU 🔥</h1>", unsafe_allow_html=True)
