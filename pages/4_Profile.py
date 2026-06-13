import streamlit as st

from frontend.components import page_header, section_title
from frontend.styles import load_css
from frontend.ui import render_navbar, require_username
from frontend.chatbot import chatbot_ui

st.set_page_config(
    page_title="Profile",
    page_icon=":user:",
    layout="wide",
)

load_css()
render_navbar("Profile")
require_username(force=True)

username = st.session_state.get("username", "Unknown User")

# Display the custom welcome message exactly once after sign up
if st.session_state.get("new_account"):
    st.html(f"""
    <div class="glass-card" style="padding: 24px; border-left: 4px solid var(--leaf-primary); margin-bottom: 24px; display: flex; align-items: center; gap: 16px;">
        <div style="font-size: 28px; color: var(--leaf-primary); display: flex; align-items: center; justify-content: center; width: 64px; height: 64px; background: rgba(34, 197, 94, 0.1); border-radius: 50%;">
            <i class="fa-solid fa-seedling"></i>
        </div>
        <div>
            <h3 style="margin: 0; font-size: 20px; color: var(--leaf-text); font-family: 'Poppins', sans-serif;">Account Created Successfully!</h3>
            <p style="margin: 4px 0 0 0; color: var(--leaf-muted); font-size: 15px;">Welcome to AgroVision AI, <strong>{username}</strong>. Your profile is all set up and ready to go.</p>
        </div>
    </div>
    """)
    st.session_state.new_account = False

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