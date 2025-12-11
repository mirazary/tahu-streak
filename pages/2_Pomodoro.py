import streamlit as st
import time

st.set_page_config(page_title="Pomodoro", page_icon="⏱️", layout="wide")

st.markdown("""
<style>
body { background:#ffffff; font-family:'Inter', sans-serif; }
.title { font-size:28px; font-weight:800; color:#0078FF; text-align:center; }
.subt  { font-size:16px; font-weight:500; color:#333; text-align:center; }
.timer { font-size:64px; font-weight:900; color:#FF3D00; text-align:center; margin-top:10px; }
div.stButton > button {
  background:#0078FF;
  color:#fff;
  border:none;
  font-weight:700;
  border-radius:8px;
  padding:10px 20px;
  font-size:16px;
  box-shadow:2px 2px 6px rgba(0,0,0,0.1);
}
div.stButton > button:hover {
  background:#0065d1;
}
</style>
""", unsafe_allow_html=True)

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("Kamu belum login. Silakan kembali ke halaman utama.")
    st.stop()

st.session_state.setdefault("pomodoro_running", False)
st.session_state.setdefault("pomodoro_completed", False)

st.markdown("<h1 class='title'>⏱️ Sesi Pomodoro</h1>", unsafe_allow_html=True)
st.markdown("<p class='subt'>Fokus selama 25 menit penuh untuk menjaga streak-mu tetap menyala 🔥</p>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

col_left, col_center, col_right = st.columns([1, 2, 1])

with col_center:
    # sebelum mulai
    if not st.session_state.pomodoro_running and not st.session_state.pomodoro_completed:
        st.markdown("<br><br>", unsafe_allow_html=True)
        if st.button("Mulai Fokus Sekarang", use_container_width=True):
            st.session_state.pomodoro_running = True
            st.session_state.pomodoro_completed = False
            st.rerun()

    # countdown berjalan
    elif st.session_state.pomodoro_running:
        st.info("Pomodoro sedang berjalan... tetap fokus 💪")
        placeholder = st.empty()
        progress = st.progress(0)
        total_time = 1500

        for i in range(total_time):
            minutes = (total_time - i) // 60
            seconds = (total_time - i) % 60
            timer_text = f"{minutes:02d}:{seconds:02d}"
            placeholder.markdown(f"<p class='timer'>{timer_text}</p>", unsafe_allow_html=True)
            progress.progress((i + 1) / total_time)
            time.sleep(1)

        st.session_state.pomodoro_running = False
        st.session_state.pomodoro_completed = True
        st.rerun()

    # selesai
    else:
        st.success("🎉 Sesi Pomodoro telah selesai! Kamu hebat!")
        if st.button("Kembali ke Dashboard", use_container_width=True):
            st.switch_page("pages/1_Dashboard.py")

st.markdown(
    """
    <hr style='margin-top:40px; border:1px solid #eee;'>
    <p style='text-align:center; font-size:13px; color:#888;'>
        © 2025 <b>MIWZAAR</b> — All rights reserved.
    </p>
    """,
    unsafe_allow_html=True
)
