import streamlit as st
from streamlit_oauth import OAuth2Component
import requests

def oauth2_login():
    oauth2 = OAuth2Component(
        client_id=st.secrets["GOOGLE_CLIENT_ID"],
        client_secret=st.secrets["GOOGLE_CLIENT_SECRET"],
        authorize_endpoint="https://accounts.google.com/o/oauth2/v2/auth",
        token_endpoint="https://oauth2.googleapis.com/token",
    )

    result = oauth2.authorize_button(
        "Login",
        redirect_uri = st.secrets["REDIRECT_URI"]
        scope="openid email profile",
        key="google_login"
    )

    if not result:
        return None

    token = result.get("token", {})
    access_token = token.get("access_token")

    if not access_token:
        return None

    # Request userinfo endpoint
    userinfo = requests.get(
        "https://openidconnect.googleapis.com/v1/userinfo",
        headers={"Authorization": f"Bearer {access_token}"}
    ).json()

    return {
        "email": userinfo.get("email"),
        "name": userinfo.get("name")
    }

