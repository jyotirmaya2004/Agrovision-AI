import os
import pandas as pd
import streamlit as st
from dotenv import load_dotenv

from frontend.components import page_header, get_confidence_color
from frontend.styles import load_css
from frontend.ui import render_navbar
from frontend.chatbot import chatbot_ui

st.set_page_config(
    page_title="Admin - Database Viewer",
    page_icon=":shield:",
    layout="wide",
    initial_sidebar_state="collapsed",
)

load_css()
render_navbar("Admin")
page_header(
    "Admin - Database Viewer",
    "View the Supabase database records directly from the deployed app.",
    "fa-shield-halved",
)

load_dotenv()
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")

if not st.session_state.get("admin_authenticated", False):
    st.html(
        """
        <div class="glass-card" style="padding: 40px 24px; text-align: center; margin-bottom: 32px; margin-top: 16px; border-top: 3px solid #ef4444;">
            <div style="display: inline-flex; align-items: center; justify-content: center; width: 64px; height: 64px; border-radius: 50%; background: rgba(239, 68, 68, 0.1); color: #ef4444; font-size: 28px; margin-bottom: 16px;">
                <i class="fa-solid fa-lock"></i>
            </div>
            <h1 style="margin: 0 0 12px 0; font-family: 'Poppins', sans-serif; font-size: 32px !important; color: var(--leaf-text);">Admin Access Restricted</h1>
            <p style="margin: 0; color: var(--leaf-muted); font-size: 18px; max-width: 600px; margin-left: auto; margin-right: auto;">Please enter the master admin password to access the database viewer.</p>
        </div>
        """
    )
    auth_container = st.container()
    with auth_container:
        st.markdown('<div class="auth-container-marker"></div>', unsafe_allow_html=True)
        st.html('<h4 style="margin-top: 0; margin-bottom: 16px; color: var(--leaf-text); font-family: \'Poppins\', sans-serif;"><i class="fa-solid fa-key" style="color: #ef4444; margin-right: 8px;"></i> Admin Authentication</h4>')
        pwd = st.text_input("Admin Password", type="password", placeholder="Enter admin password", label_visibility="collapsed", key="admin_pass")

        st.markdown('<div class="admin-unlock-marker"></div>', unsafe_allow_html=True)
        if st.button("Unlock Dashboard", type="primary", use_container_width=True):
            if pwd == ADMIN_PASSWORD:
                st.session_state.admin_authenticated = True
                st.rerun()
            else:
                st.error("Incorrect admin password.")

    # Render chatbot and stop execution so the database remains hidden
    chatbot_ui()
    st.stop()

st.markdown('<div class="admin-lock-marker"></div>', unsafe_allow_html=True)
if st.button("Lock Dashboard", key="lock_dashboard"):
    st.session_state.admin_authenticated = False
    st.rerun()

try:
    from backend.db import get_all_predictions, delete_prediction, delete_all_predictions
    response = get_all_predictions()
    df = pd.DataFrame(response.data)

    if not df.empty:
        # Flatten the nested dictionary from the foreign key join
        df["username"] = df["app_users"].apply(lambda x: x.get("username") if isinstance(x, dict) else "Unknown")
        df = df.drop(columns=["app_users"])
        # Reorder columns for better readability
        cols = ["id", "username", "timestamp", "disease", "confidence", "image_url", "user_id"]
        df = df[[c for c in cols if c in df.columns]]
    else:
        df = pd.DataFrame(columns=["id", "username", "timestamp", "disease", "confidence", "image_url", "user_id"])

    st.write(f"### Total Records: {len(df)}")

    def color_confidence(val):
        try:
            return f'color: {get_confidence_color(float(val))}'
        except Exception:
            return ''

    styled_df = df.style.map(color_confidence, subset=['confidence'])

    st.dataframe(
        styled_df,
        use_container_width=True,
        column_config={
            "image_url": st.column_config.ImageColumn("Uploaded Image"),
            "confidence": st.column_config.NumberColumn("Confidence", format="%.2f%%")
        }
    )

    if not df.empty:
        st.write("#### Manage Records")
        col_sel, col_btn_del, col_btn_all = st.columns([2, 1, 1])
        with col_sel:
            row_id = st.selectbox("Select Record ID to delete", df["id"].tolist(), label_visibility="collapsed")
        with col_btn_del:
            if st.button("Delete Row", use_container_width=True):
                delete_prediction(row_id)
                st.rerun()
        with col_btn_all:
            confirm_delete = st.checkbox("Confirm wipe", help="Check this box to enable the delete button")
            if st.button("Delete ALL", type="primary", use_container_width=True, disabled=not confirm_delete):
                delete_all_predictions()
                st.rerun()
        st.html("<br>")

except Exception as e:
    st.error(f"Could not load database: {e}")

# Render floating chatbot globally
chatbot_ui()