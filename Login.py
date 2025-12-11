import streamlit as st
from modules.auth import oauth2_login
from modules.ui import display_logo_center  

st.set_page_config(
    page_title="TAHU",
    page_icon="🔥",
    layout="wide",
)

st.markdown("""
<style>
body {
    background-color: #ffffff;
}
</style>
""", unsafe_allow_html=True)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def render_login_page():
    col_left, col_center, col_right = st.columns([1.5, 5, 1.5])

    with col_center:
        st.markdown("<br>", unsafe_allow_html=True)
        display_logo_center()

        st.markdown(
            """
            <h1 style='text-align:center; font-weight:800; color:#0078FF; font-size:32px;'>
                🔑 Masuk ke Dunia TAHU
            </h1>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <p style='text-align:center; font-size:15px; color:#222831; line-height:1.5;'>
                <b>TAHU (Tugas Akhir Harus Usai)</b> teman seperjuanganmu dalam menyelesaikan Tugas Akhir dengan semangat dan konsistensi. 
                <br>
                Yuk, mulai petualanganmu bersama Pet TAHU dan jaga streak-mu setiap hari! 🔥
            </p>
            """,
            unsafe_allow_html=True
        )

        st.markdown("<br>", unsafe_allow_html=True)

        card1, card2, card3 = st.columns([1, 4, 1])
        with card2:
            with st.container(border=True):
                st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)

                st.markdown(
                    """
                    <p style='text-align:center; font-weight:700; font-size:28px; color:#222831;'>
                        Google Sign-In
                    </p>
                    """,
                    unsafe_allow_html=True
                )

                st.markdown(
                    """
                    <div style="
                        background-color:#E3F2FD;
                        border-left: 4px solid #0078FF;
                        padding: 8px 12px;
                        border-radius: 6px;
                        font-size: 13px;
                        color: #0D47A1;
                        margin: 10px 0;
                    ">
                        🛡️ Autentikasi diperlukan untuk menyimpan progress streak harianmu.
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                btn1, btn2, btn3 = st.columns([1, 1, 1])
                with btn2:
                    result = oauth2_login()

                if result:
                    st.session_state.user_name = result["name"]
                    st.session_state.user_email = result["email"]
                    st.session_state.logged_in = True
                    st.rerun()

                st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)

st.markdown("<br><p style='text-align:center; color:#aaa;'>© 2025 MIWZAAR · TAHU Project</p>", unsafe_allow_html=True)

if st.session_state.logged_in:
    st.switch_page("pages/1_Home.py")
else:
    render_login_page()
