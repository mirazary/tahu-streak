import streamlit as st
import os
from modules.gacha import roll_gacha, get_history
import base64

st.set_page_config(page_title="Gacha", page_icon="🎲", layout="wide")

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("Anda belum login. Silakan login terlebih dahulu.")
    st.stop()

email = st.session_state.user_email

st.markdown(
    "<h1 style='text-align:center; font-weight:800;'>🎲 GACHA TAHU</h1>",
    unsafe_allow_html=True
)
st.markdown(
    "<p style='text-align:center; color:#444;'>Coba keberuntunganmu hari ini dan dapatkan hadiah random dari semesta TAHU 🌟</p>",
    unsafe_allow_html=True
)
st.divider()

def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

col_left, col_center, col_right = st.columns([1, 2, 1])

with col_center:
    if st.button("🎁 Buka Gacha Hari Ini", use_container_width=True):
        rarity, reward, success = roll_gacha(email)

        if not success:
            st.warning("Kamu sudah gacha hari ini 😅")
        else:
            img_map = {
                "Common": "assets/gacha/common.png",
                "Rare": "assets/gacha/rare.png",
                "Epic": "assets/gacha/epic.png",
                "Legendary": "assets/gacha/legendary.png"
            }

            img_path = img_map.get(rarity, "assets/gacha/common.png")
            img_base64 = get_base64_image(img_path)
            st.balloons()

            rarity_colors = {
                "Common": "#555",
                "Rare": "#3B82F6",
                "Epic": "#9333EA",
                "Legendary": "#FACC15"
            }

            text_color = rarity_colors.get(rarity, "#333")

            if img_base64:
                st.markdown(f"""
                <div style='text-align:center; padding:20px;'>
                    <img src='data:image/png;base64,{img_base64}' width='300'
                         style='border-radius:10px; box-shadow:4px 4px #222; animation:pop 0.6s ease;'/>
                    <h2 style='font-weight:900; margin-top:10px; color:{text_color};'>{rarity} ✨</h2>
                    <p style='font-size:18px; font-weight:700; color:#444;'>{reward}</p>
                </div>
                <style>
                @keyframes pop {{
                    0% {{ transform: scale(0.6); opacity: 0; }}
                    70% {{ transform: scale(1.1); opacity: 1; }}
                    100% {{ transform: scale(1); }}
                }}
                </style>
                """, unsafe_allow_html=True)
            else:
                st.warning(f"Gambar {rarity} tidak ditemukan di {img_path}.")

st.markdown("<hr><h3>🎟️ Riwayat Gacha Terakhir</h3>", unsafe_allow_html=True)
history = get_history(email)

if history.empty:
    st.info("Belum ada hasil gacha nih 😋")
else:
    for _, row in history.iterrows():
        rarity = row["rarity"]
        reward = row["reward"]
        img_map = {
            "Common": "assets/gacha/common.png",
            "Rare": "assets/gacha/rare.png",
            "Epic": "assets/gacha/epic.png",
            "Legendary": "assets/gacha/legendary.png"
        }
        img_path = img_map.get(rarity, "assets/gacha/common.png")

        col1, col2 = st.columns([1, 4])
        with col1:
            st.image(img_path, width=80)
        with col2:
            st.markdown(f"**{rarity}** — {reward}")

st.markdown("<br><p style='text-align:center; color:#aaa;'>© 2025 MIWZAAR · TAHU Project</p>", unsafe_allow_html=True)
