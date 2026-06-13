import streamlit as st

from frontend.components import page_header, section_title
from frontend.styles import load_css
from frontend.ui import render_navbar, require_username
from frontend.chatbot import chatbot_ui

st.set_page_config(
    page_title="Profile",
    page_icon=":user:",
    layout="wide",
    initial_sidebar_state="collapsed",
)

load_css()
render_navbar("Profile")
require_username(force=True)

username = st.session_state.get("username", "Unknown User")

page_header(
    "User Profile",
    "View and manage your account details.",
    "fa-user",
)

section_title("Account Details", "fa-id-card")

user_id = st.session_state.get("user_id")
avatar = st.session_state.get("avatar", "🧑‍🌾")

col1, col2 = st.columns([1, 3])
with col1:
    st.html(f"""
    <div style="text-align: center; padding: 20px; background: rgba(34, 197, 94, 0.1); border-radius: 50%; width: 150px; height: 150px; margin: 0 auto; display: flex; align-items: center; justify-content: center; font-size: 80px;">
        {avatar}
    </div>
    """)
with col2:
    st.write(f"### {username}")
    st.write(f"**User ID:** {user_id}")
    st.write("**Account Status:** Active")

chatbot_ui()