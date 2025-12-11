import streamlit as st
import os
import pandas as pd
import time
from modules.streak import load_streak, checkin_today

st.set_page_config(page_title="Home", page_icon="🔥", layout="wide")

st.markdown("""
<style>
body { background:#ffffff; font-family:'Inter', sans-serif; }

.title { font-size:28px; font-weight:800; color:#222831; text-align:center; }
.subt  { font-size:16px; font-weight:500; color:#333; text-align:center; }
.big   { font-size:56px; font-weight:900; color:#0078FF; text-align:center; }

.lb {
  background:#f8f8f8;
  border:2px solid #E0E0E0;
  border-radius:8px;
  padding:14px;
  margin:8px;
  box-shadow:2px 2px 6px rgba(0,0,0,0.05);
  text-align:center;
}

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
#pomodoro-btn button { background:#FF3D00 !important; color:#fff !important; }
#checkin-btn button { background:#00C853 !important; color:#fff !important; }
#locked-btn button { background:#ccc !important; color:#666 !important; border-color:#aaa !important; }
</style>
""", unsafe_allow_html=True)

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("Kamu belum login. Silakan kembali ke halaman utama.")
    st.stop()

st.session_state.setdefault("pomodoro_completed", False)
st.session_state.setdefault("pomodoro_running", False)

def start_pomodoro():
    st.session_state.pomodoro_running = True
    st.info("⏱️ Pomodoro dimulai! Fokus selama 3 detik (simulasi 25 menit).")
    ph = st.empty()
    for i in range(3, 0, -1):
        ph.markdown(f"<h2 style='text-align:center; color:#0078FF'>{i}</h2>", unsafe_allow_html=True)
        time.sleep(1)
    ph.empty()
    st.session_state.pomodoro_running = False
    st.session_state.pomodoro_completed = True
    st.success("✅ Pomodoro selesai. Check-in aktif.")
    st.balloons()
    st.rerun()

with st.sidebar:
    st.image("assets/logo/tahu_logo.png", use_container_width=True)
    st.markdown("---")
    st.markdown(f"**{st.session_state.user_name}**")
    st.caption(st.session_state.user_email)
    st.markdown("---")
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.clear()
        st.switch_page("Login.py")

st.markdown("<h1 class='title'> Rumah TAHU</h1>", unsafe_allow_html=True)
st.markdown(f"<p class='subt'>Selamat datang, <b>{st.session_state.user_name}</b> 👋</p>", unsafe_allow_html=True)
st.divider()

col1, col2 = st.columns([1, 1.2])

email = st.session_state.user_email
streak, last_checkin_str = load_streak(email)
badge = "Bronze 🥉" if streak < 5 else "Silver 🥈" if streak < 10 else "Gold 🥇"

# PET
with col1:
    st.markdown("<p class='title' style='font-size:22px'>🐾 PET</p>", unsafe_allow_html=True)
    # Menentukan gambar pet berdasarkan streak
    # Menentukan pet berdasarkan streak
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

    # Menampilkan gambar dan kondisi
    if os.path.exists(pet_path):
        col_img_l, col_img_c, col_img_r = st.columns([1, 0.8, 1])
        with col_img_c:
            st.image(pet_path, width=130)
    else:
        st.warning("Gambar pet tidak ditemukan!")

    st.markdown(f"<p class='subt'>{pet_name}</p>", unsafe_allow_html=True)
    st.markdown(f"<p class='subt'>Kondisi: {pet_condition}</p>", unsafe_allow_html=True)



# STREAK
with col2:
    st.markdown("<p class='title' style='font-size:22px'>🔥 STREAK</p>", unsafe_allow_html=True)
    st.markdown(f"<p class='big'>{streak}</p>", unsafe_allow_html=True)
    st.markdown("<p class='subt'>Hari berturut-turut</p>", unsafe_allow_html=True)
    st.markdown(f"<p class='subt'><b>Rank:</b> {badge}</p>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    b1, b2, b3 = st.columns([1, 2, 1])
    with b2:
        if st.session_state.pomodoro_running:
            st.button("⏱️ Sedang Bekerja...", key="locked-btn", use_container_width=True, disabled=True)
        elif not st.session_state.pomodoro_completed:
            if st.button("Mulai Pomodoro", key="pomodoro-btn", use_container_width=True):
                st.switch_page("pages/2_Pomodoro.py")
        else:
            last_date = pd.to_datetime(last_checkin_str).date() if last_checkin_str else None
            is_checked_in = (last_date == pd.Timestamp.now().date())
            if is_checked_in:
                st.button("Sudah Check-in", key="locked-btn", use_container_width=True, disabled=True)
            else:
                if st.button("Check-in Hari Ini!", key="checkin-btn", use_container_width=True):
                    new_streak, success = checkin_today(email)
                    if success:
                        st.session_state.pomodoro_completed = False
                        st.success(f"Streak naik ke {new_streak} hari!")
                    else:
                        st.info("Sudah Check-in hari ini.")
                    st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

try:
    df = pd.read_csv("data/streak.csv").sort_values("streak", ascending=False).head(6)
except:
    df = pd.DataFrame(columns=["email", "streak"])

# --- Footer ---
st.markdown("<br><p style='text-align:center; color:#aaa;'>© 2025 MIWZAAR · TAHU Project</p>", unsafe_allow_html=True)

