import streamlit as st
import os
import pandas as pd
from modules.streak import load_streak
from modules.progress import has_logged_today

st.set_page_config(page_title="Home", page_icon="🔥", layout="wide")

# ===== CSS STYLE =====
st.markdown("""
<style>
body { background:#ffffff; font-family:'Inter', sans-serif; }

.title { font-size:28px; font-weight:800; color:#222831; text-align:center; }
.subt  { font-size:16px; font-weight:500; color:#333; text-align:center; }
.big   { font-size:56px; font-weight:900; color:#0078FF; text-align:center; }

div.stButton > button {
  background:#EAEAEA;
  color:#000;
  border:2px solid #000;
  border-radius:8px;
  font-weight:700;
  padding:10px 18px;
  font-size:15px;
}
div.stButton > button:hover {
  background:#f5f5f5;
  transform:translate(1px,1px);
  box-shadow:1px 1px 2px rgba(0,0,0,0.2);
}

#checkin-btn button { background:#00C853 !important; color:#fff !important; }
#locked-btn button { background:#ccc !important; color:#666 !important; border-color:#aaa !important; }
</style>
""", unsafe_allow_html=True)

# ===== AUTH CHECK =====
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("Kamu belum login. Silakan kembali ke halaman utama.")
    st.stop()

# ===== SIDEBAR =====
with st.sidebar:
    st.image("assets/logo/tahu_logo.png", use_container_width=True)
    st.markdown("---")
    st.markdown(f"**{st.session_state.user_name}**")
    st.caption(st.session_state.user_email)
    st.markdown("---")
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.clear()
        st.switch_page("Login.py")

# ===== HEADER =====
st.markdown("<h1 class='title'>Rumah TAHU</h1>", unsafe_allow_html=True)
st.markdown(f"<p class='subt'>Selamat datang, <b>{st.session_state.user_name}</b> 👋</p>", unsafe_allow_html=True)
st.divider()

# ===== CONTENT =====
col1, col2 = st.columns([1, 1.2])
email = st.session_state.user_email

streak, _ = load_streak(email)
badge = "Bronze 🥉" if streak < 5 else "Silver 🥈" if streak < 10 else "Gold 🥇"

# ===== PET SECTION =====
with col1:
    st.markdown("<p class='title' style='font-size:22px'>🐾 PET</p>", unsafe_allow_html=True)

    # Tentukan gambar pet
    if streak < 5:
        pet_path = "assets/pets/pet_stage1.png"
        pet_name = "Level 1 — Tahu Polos"
        pet_condition = "Lapar tapi semangat 💪"
    elif streak < 10:
        pet_path = "assets/pets/pet_stage2.png"
        pet_name = "Level 2 — Tahu Berbumbu"
        pet_condition = "Berenergi dan produktif ⚡"
    else:
        pet_path = "assets/pets/pet_stage3.png"
        pet_name = "Level 3 — Tahu Legendaris"
        pet_condition = "Bahagia dan termotivasi 🌟"

    # Tampilkan gambar
    if os.path.exists(pet_path):
        _, center, _ = st.columns([1, 1, 1])
        with center:
            st.image(pet_path, width=130)
    else:
        st.warning("Gambar pet tidak ditemukan!")

    st.markdown(f"<p class='subt'>{pet_name}</p>", unsafe_allow_html=True)
    st.markdown(f"<p class='subt'>Kondisi: {pet_condition}</p>", unsafe_allow_html=True)

# ===== STREAK SECTION =====
with col2:
    st.markdown("<p class='title' style='font-size:22px'>🔥 STREAK</p>", unsafe_allow_html=True)
    st.markdown(f"<p class='big'>{streak}</p>", unsafe_allow_html=True)
    st.markdown("<p class='subt'>Hari berturut-turut</p>", unsafe_allow_html=True)
    st.markdown(f"<p class='subt'><b>Rank:</b> {badge}</p>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # STATUS CHECK-IN BERDASARKAN PROGRESS
    is_checked_in = has_logged_today(email)

    _, mid, _ = st.columns([1, 2, 1])
    with mid:
        if is_checked_in:
            st.button("Sudah Check-in Hari Ini", key="locked-btn", use_container_width=True, disabled=True)
        else:
            if st.button("Isi Progress Harian 🔥", key="checkin-btn", use_container_width=True):
                st.switch_page("pages/7_Progress.py")

# ===== FOOTER =====
st.markdown("<br><p style='text-align:center; color:#aaa;'>© 2025 MIWZAAR · TAHU Project</p>", unsafe_allow_html=True)
