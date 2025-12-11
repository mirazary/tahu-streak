import streamlit as st
from modules.friends import add_friend, get_friends

st.set_page_config(page_title="Teman TAHU", page_icon="🤝", layout="wide")

# --- CSS ---
st.markdown("""
<style>
body { background-color: #ffffff; color: #222; font-family: "Poppins", sans-serif; }

h1 {
    color: #0078FF;
    font-weight: 800;
    text-align: center;
    margin-bottom: 5px;
}

.subhead {
    text-align: center;
    color: #666;
    font-size: 15px;
    margin-top: -5px;
    margin-bottom: 25px;
}

.friend-card {
    background: #f9f9f9;
    border: 2px solid #e0e0e0;
    border-radius: 10px;
    padding: 14px 16px;
    margin: 10px 0;
    box-shadow: 3px 3px #d9d9d9;
    transition: all 0.2s ease-in-out;
}
.friend-card:hover {
    background: #eef6ff;
    box-shadow: 4px 4px #0078FF;
    transform: translateY(-2px);
}
.add-box {
    background-color: #f7faff;
    border: 2px dashed #0078FF;
    border-radius: 10px;
    padding: 20px;
    box-shadow: 2px 2px #d9d9d9;
}
.stButton>button {
    background-color: #0078FF;
    color: #fff;
    border: 2px solid #000;
    font-weight: 700;
    border-radius: 6px;
    box-shadow: 3px 3px #000;
    transition: all 0.2s ease;
}
.stButton>button:hover {
    background-color: #339CFF;
    transform: translate(2px, 2px);
    box-shadow: 1px 1px #000;
}
</style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown("<h1>Teman TAHU</h1>", unsafe_allow_html=True)
st.markdown("<p class='subhead'>Jaga semangat bareng teman seperjuangan Tugas Akhir 💪</p>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

email = st.session_state.user_email

# --- Layout 2 kolom ---
col_add, col_list = st.columns([1.2, 1.5])

with col_add:
    st.markdown("<h3 style='text-align:center;'>Tambah Teman</h3>", unsafe_allow_html=True)
    with st.container(border=True):
        friend_email = st.text_input("Masukkan email temanmu:")
        if st.button("Tambahkan Teman"):
            if friend_email == email:
                st.warning("Tidak bisa menambahkan diri sendiri 😅")
            elif add_friend(email, friend_email):
                st.success(f"{friend_email} berhasil ditambahkan!")
            else:
                st.info("Kamu sudah berteman dengan dia.")

with col_list:
    st.markdown("<h3 style='text-align:center;'>Daftar Teman Aktif</h3>", unsafe_allow_html=True)
    friends = get_friends(email)

    if len(friends) > 0:
        for _, row in friends.iterrows():
            st.markdown(f"""
            <div class='friend-card'>
                <h4 style='margin:0; color:#0078FF;'>{row['friend']}</h4>
                <p style='margin:2px 0; color:#444;'>🔥 Streak bareng: <b>{row['streak']} hari</b></p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Belum punya teman yang nyalain api bareng 😅")

# --- Footer ---
st.markdown("<br><p style='text-align:center; color:#aaa;'>© 2025 MIWZAAR · TAHU Project</p>", unsafe_allow_html=True)
