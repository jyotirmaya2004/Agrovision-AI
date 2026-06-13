import streamlit as st

from frontend.components import page_header, section_title
from frontend.styles import load_css
from frontend.ui import render_navbar
from frontend.chatbot import chatbot_ui


st.set_page_config(
    page_title="About Project",
    page_icon=":information_source:",
    layout="wide",
    initial_sidebar_state="collapsed",
)

load_css()
render_navbar("About")
page_header(
    "About Plantexa AI",
    "An AI-powered plant leaf disease detection system with practical crop-care guidance.",
    "fa-circle-info",
)

section_title("Project Overview", "fa-leaf")
st.html(
    """
    <div class="glass-card" style="padding: 24px; margin-bottom: 24px;">
        <p style="color: var(--leaf-muted); font-size: 16px; margin: 0;">
            Plantexa AI uses a two-stage deep learning workflow. It first checks
            whether the uploaded image looks like a plant leaf, then predicts the
            most likely disease and shows symptoms, causes, treatment, and prevention
            guidance from the disease knowledge base.
        </p>
    </div>
    """,
)

col_frontend, col_backend, col_model = st.columns(3)
with col_frontend:
    st.html(
        """
        <div class="glass-card" style="padding: 24px; height: 100%;">
            <h3 style="margin-top: 0; color: var(--leaf-primary); font-family: 'Poppins', sans-serif;"><i class="fa-solid fa-desktop"></i> Frontend</h3>
            <ul style="color: var(--leaf-muted); font-size: 15px; padding-left: 20px;">
                <li style="margin-bottom: 8px;">Streamlit</li>
                <li style="margin-bottom: 8px;">HTML components</li>
                <li>Modern Glassmorphism CSS</li>
            </ul>
        </div>
        """,
    )

with col_backend:
    st.html(
        """
        <div class="glass-card" style="padding: 24px; height: 100%;">
            <h3 style="margin-top: 0; color: var(--leaf-primary); font-family: 'Poppins', sans-serif;"><i class="fa-solid fa-server"></i> Backend</h3>
            <ul style="color: var(--leaf-muted); font-size: 15px; padding-left: 20px;">
                <li style="margin-bottom: 8px;">Python</li>
                <li style="margin-bottom: 8px;">TensorFlow</li>
                <li>NumPy & Pandas</li>
            </ul>
        </div>
        """,
    )

with col_model:
    st.html(
        """
        <div class="glass-card" style="padding: 24px; height: 100%;">
            <h3 style="margin-top: 0; color: var(--leaf-primary); font-family: 'Poppins', sans-serif;"><i class="fa-solid fa-brain"></i> Models</h3>
            <ul style="color: var(--leaf-muted); font-size: 15px; padding-left: 20px;">
                <li style="margin-bottom: 8px;">MobileNetV2 classifier</li>
                <li style="margin-bottom: 8px;">Leaf validation network</li>
                <li>224 x 224 resolution</li>
            </ul>
        </div>
        """,
    )

section_title("Project Features", "fa-list-check")
st.html(
    """
    <div class="glass-card" style="padding: 24px; margin-bottom: 32px;">
        <ul style="color: var(--leaf-muted); font-size: 16px; margin: 0; padding-left: 20px; line-height: 1.8;">
            <li><strong>Two-Stage Pipeline:</strong> Leaf detection before disease classification</li>
            <li><strong>AI Analysis:</strong> Top 3 predictions with real-time confidence scores</li>
            <li><strong>Knowledge Base:</strong> Detailed disease symptoms, causes, treatment, and prevention</li>
            <li><strong>NVIDIA LLM:</strong> Context-aware AI agriculture assistant</li>
            <li><strong>Reporting:</strong> Downloadable PDF report cards and session prediction history</li>
        </ul>
    </div>
    """,
)

section_title("Academic Details", "fa-graduation-cap")

st.html(
    """
    <div class="glass-card" style="padding: 24px; margin-bottom: 32px;">
        <h4 style="margin-top: 0; color: var(--leaf-text); font-family: 'Poppins', sans-serif;">Project Team Members</h4>
        <ul style="color: var(--leaf-muted); font-size: 16px; line-height: 1.8; margin-bottom: 24px; padding-left: 20px;">
            <li><strong>Jyotirmaya Behera</strong> (3146/24)</li>
            <li><strong>Diptesh Ranjan Pradhan</strong> (3141/24)</li>
            <li><strong>Bibekananda Sahoo</strong> (3136/24)</li>
            <li><strong>Pritam Kumar Behera</strong> (3159/24)</li>
            <li><strong>Laxman Kumar Sahoo</strong> (3148/24)</li>
        </ul>

        <h4 style="margin-top: 0; color: var(--leaf-text); font-family: 'Poppins', sans-serif;">Academic Information</h4>
        <p style="color: var(--leaf-muted); font-size: 16px; margin: 0;"><strong>Academic Year:</strong> 2025 - 2026</p>
    </div>
    """
)

# Render floating chatbot globally
chatbot_ui()
