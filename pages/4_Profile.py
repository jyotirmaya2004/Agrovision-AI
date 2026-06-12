import os
import streamlit as st
from frontend.components import page_header
from frontend.styles import load_css
from frontend.ui import require_username
from frontend.chatbot import chatbot_ui

st.set_page_config(
    page_title="User Profile",
    page_icon=":user:",
    layout="wide"
)

load_css()
require_username(force=True)

page_header(
    "User Profile",
    "Manage your account details and view your activity statistics.",
    "fa-user"
)

user_id = st.session_state.get("user_id")
username = st.session_state.get("username", "User")
avatar = st.session_state.get("avatar", "🧑‍🌾")

created_at = "Unknown"
total_scans = 0

try:
    from supabase import create_client
    supabase_url = os.getenv("SUPABASE_URL", "")
    supabase_key = os.getenv("SUPABASE_KEY", "")
    if supabase_url and supabase_key:
        supabase = create_client(supabase_url, supabase_key)

        user_res = supabase.table("app_users").select("created_at").eq("id", user_id).execute()
        if user_res.data:
            created_at = user_res.data[0].get("created_at", "Unknown")[:10]

        hist_res = supabase.table("user_predictions").select("id", count="exact").eq("user_id", user_id).execute()
        if hist_res.count is not None:
            total_scans = hist_res.count
except Exception:
    pass

col1, col2 = st.columns([1, 2], gap="large")
with col1:
    st.html(f"""
    <div class="glass-card" style="padding: 32px; text-align: center; border-top: 3px solid var(--leaf-primary);">
        <div style="font-size: 80px; margin-bottom: 16px; filter: drop-shadow(0 4px 6px rgba(0,0,0,0.2));">{avatar}</div>
        <h2 style="margin: 0; color: var(--leaf-text); font-family: 'Poppins', sans-serif;">{username}</h2>
        <p style="color: var(--leaf-muted); font-size: 14px;">Member since: {created_at}</p>
    </div>
    """)
with col2:
    st.html(f"""
    <div class="glass-card" style="padding: 32px; height: 100%;">
        <h3 style="margin-top: 0; color: var(--leaf-primary); font-family: 'Poppins', sans-serif;"><i class="fa-solid fa-chart-simple"></i> Activity Statistics</h3>
        <div style="display: grid; grid-template-columns: 1fr; gap: 16px; margin-top: 24px;">
            <div style="background: rgba(255,255,255,0.05); padding: 24px; border-radius: 12px; text-align: center; border: 1px solid var(--leaf-border);">
                <i class="fa-solid fa-microscope" style="font-size: 32px; color: var(--leaf-primary); margin-bottom: 12px;"></i>
                <h2 style="margin: 0; font-size: 36px; color: var(--leaf-text);">{total_scans}</h2>
                <p style="margin: 0; color: var(--leaf-muted); font-weight: 600;">Total AI Scans Completed</p>
            </div>
        </div>
    </div>
    """)

# Render floating chatbot globally
chatbot_ui()