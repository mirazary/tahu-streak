import streamlit as st
import os
from modules.streak import load_streak
from modules.pet import get_pet_stage, load_pet, update_pet
from modules.utils import asset_path
import base64

st.set_page_config(page_title="Pet", page_icon="🐾", layout="wide")

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("Anda belum login. Silakan kembali ke halaman utama.")
    st.stop()

email = st.session_state.user_email
streak, _ = load_streak(email)
stage, stage_name, mood = get_pet_stage(streak)
level, exp = load_pet(email)
update_pet(email, stage, exp + 1)

img_path = asset_path("pets", f"pet_stage{stage}.png")

# 🌈 CSS ANIMASI PET
st.markdown("""
<style>
@keyframes bounce {
  0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
  40% { transform: translateY(-20px); }
  60% { transform: translateY(-10px); }
}

.pet-container {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 30px;
}

.pet-img {
  width: 280px;
  animation: bounce 2.5s infinite;
  transition: transform 0.2s ease-in-out;
}

.pet-img:hover {
  transform: scale(1.05) rotate(2deg);
  animation-play-state: paused;
}

.pet-info {
  text-align: center;
  color: #1f2a44;
}

.pet-info h2 {
  font-weight: 900;
  margin-bottom: 5px;
}

.pet-info p {
  font-size: 16px;
  margin: 0;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center; font-weight:800;'>🐾 PET TAHU</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#555;'>Temui sahabat TAHU-mu yang selalu setia menemanimu ngerjain TA 💪</p>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

# 🧠 Tampilan PET
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        encoded = base64.b64encode(img_file.read()).decode()
    return f"data:image/png;base64,{encoded}"

if os.path.exists(img_path):
    img_base64 = get_base64_image(img_path)
    st.markdown(f"""
    <style>
    .pet-wrapper {{
        display: flex;
        justify-content: center;
        align-items: center;
        margin-top: 30px;
    }}
    .pet-img {{
        width: 260px;
        animation: bounce 2.5s infinite;
        transition: transform 0.2s ease-in-out;
    }}
    .pet-img:hover {{
        animation-play-state: paused;
        transform: scale(1.05) rotate(3deg);
    }}
    @keyframes bounce {{
        0%, 20%, 50%, 80%, 100% {{ transform: translateY(0); }}
        40% {{ transform: translateY(-18px); }}
        60% {{ transform: translateY(-9px); }}
    }}
    </style>

    <div class="pet-wrapper">
        <img src="{img_base64}" class="pet-img" />
    </div>
    """, unsafe_allow_html=True)
else:
    st.warning(f"Gambar pet tidak ditemukan di {img_path}!")

# ℹ️ Info Pet
st.markdown(f"""
<div class="pet-info">
    <h2>{stage_name}</h2>
    <p><b>Level:</b> {stage}</p>
    <p><b>Mood:</b> {mood}</p>
    <p><b>Streak:</b> {streak} hari 🔥</p>
</div>
""", unsafe_allow_html=True)

st.markdown("<br><p style='text-align:center; color:#aaa;'>© 2025 MIWZAAR · TAHU Project</p>", unsafe_allow_html=True)
