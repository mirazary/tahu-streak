import streamlit as st
from modules.progress import save_progress, get_progress, has_logged_today
from modules.streak import load_streak, checkin_today

st.set_page_config(page_title="Progress Harian", page_icon="📝", layout="wide")

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.stop()

email = st.session_state.user_email

st.markdown("<h1 style='text-align:center;'>📝 Progress Harian</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#555;'>Catat perkembangan tugas akhirmu setiap hari!</p>", unsafe_allow_html=True)
st.markdown("---")

logged = has_logged_today(email)

if logged:
    st.success("Kamu sudah mengisi progress hari ini! 🎉")
else:
    progress = st.text_area("Apa yang kamu kerjakan hari ini?")
    duration = st.number_input("Durasi belajar (menit)", min_value=0, step=10)
    mood = st.selectbox("Mood hari ini", ["Semangat 💪", "Biasa aja 🙂", "Capek 😪", "Stress 😵"])

    if st.button("Simpan Progress"):
        ok = save_progress(email, progress, duration, mood)
        if ok:
            # Check-in streak
            checkin_today(email)
            st.success("Progress tersimpan dan streak bertambah! 🔥")
        else:
            st.warning("Kamu sudah mengisi progress hari ini.")

history = get_progress(email)

st.markdown("## Riwayat Progress")
for _, row in history.iterrows():
    st.markdown(
        f"""
        <div style='padding:10px; border:1px solid #ddd; border-radius:6px; margin-bottom:10px;'>
            <b>{row['date']}</b><br>
            📌 {row['progress']}<br>
            ⏱️ {row['duration']} menit<br>
            😊 Mood: {row['mood']}
        </div>
        """,
        unsafe_allow_html=True
    )
