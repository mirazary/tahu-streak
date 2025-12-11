import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Leaderboard", page_icon="🏅", layout="wide")

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("Kamu belum login. Silakan kembali ke halaman utama.")
    st.stop()

st.markdown("""
<style>
body { background:#ffffff; font-family:'Inter', sans-serif; }
.title { font-size:32px; font-weight:900; color:#0078FF; text-align:center; }
.lb-card {
  background:#fafafa;
  border:2px solid #E0E0E0;
  border-radius:10px;
  padding:16px;
  margin:8px;
  box-shadow:4px 4px 8px rgba(0,0,0,0.05);
  text-align:center;
  transition:all 0.2s ease-in-out;
}
.lb-card:hover {
  transform:translateY(-3px);
  box-shadow:6px 6px 10px rgba(0,0,0,0.1);
  background:#f9f9ff;
}
.rank { font-size:26px; font-weight:900; margin:0; color:#0078FF; }
.name { font-size:18px; font-weight:700; margin:4px 0; color:#222; }
.streak { font-size:16px; color:#00C853; font-weight:700; }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='title'>🏆 Leaderboard Pejuang TAHU</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#555;'>Lihat siapa yang paling konsisten nyalain streak-nya 🔥</p>", unsafe_allow_html=True)
st.divider()

# ambil data leaderboard
try:
    df = pd.read_csv("data/streak.csv").sort_values("streak", ascending=False).head(12)
except:
    st.warning("Belum ada data streak 😅")
    df = pd.DataFrame(columns=["email", "streak"])

# tampilkan leaderboard
if not df.empty:
    cols = st.columns(3)
    for i, (_, row) in enumerate(df.iterrows()):
        col = cols[i % 3]
        rank = i + 1
        icon = "👑" if rank == 1 else "🥈" if rank == 2 else "🥉" if rank == 3 else "🔥"
        col.markdown(f"""
        <div class='lb-card'>
            <p class='rank'>{icon} #{rank}</p>
            <p class='name'>{row['email'].split('@')[0]}</p>
            <p class='streak'>{row['streak']} hari</p>
        </div>
        """, unsafe_allow_html=True)
else:
    st.info("Belum ada data leaderboard.")

st.markdown("""
<hr style='margin-top:40px; border:1px solid #eee;'>
<p style='text-align:center; font-size:13px; color:#888;'>
© 2025 <b>MIWZAAR</b> — All rights reserved.
</p>
""", unsafe_allow_html=True)
