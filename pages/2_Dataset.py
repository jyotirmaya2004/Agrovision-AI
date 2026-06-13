import streamlit as st

from frontend.components import page_header, section_title
from frontend.styles import load_css
from frontend.ui import render_navbar
from frontend.chatbot import chatbot_ui


st.set_page_config(
    page_title="Dataset Information",
    page_icon=":books:",
    layout="wide",
)

load_css()
render_navbar("Dataset")
page_header(
    "Dataset Information",
    "Model training data, supported crops, and disease categories.",
    "fa-database",
)

section_title("PlantVillage Dataset", "fa-seedling")

col_summary, col_crops = st.columns([1, 1])
with col_summary:
    st.html(
        """
        <div class="glass-card" style="padding: 24px; height: 100%;">
            <h3 style="margin-top: 0; color: var(--leaf-primary); font-family: 'Poppins', sans-serif;"><i class="fa-solid fa-chart-pie"></i> Dataset Summary</h3>
            <ul style="color: var(--leaf-muted); font-size: 16px; padding-left: 20px; line-height: 1.8; margin: 0;">
                <li><strong>Total classes:</strong> 38+</li>
                <li><strong>Image format:</strong> 224 x 224 (RGB)</li>
                <li><strong>Primary purpose:</strong> Plant disease identification from leaf images</li>
                <li><strong>Source:</strong> PlantVillage & Augmented variations</li>
            </ul>
        </div>
        """,
    )

with col_crops:
    st.html(
        """
        <div class="glass-card" style="padding: 24px; height: 100%;">
            <h3 style="margin-top: 0; color: var(--leaf-primary); font-family: 'Poppins', sans-serif;"><i class="fa-solid fa-seedling"></i> Supported Crops</h3>
            <ul style="color: var(--leaf-muted); font-size: 16px; padding-left: 20px; line-height: 1.6; margin: 0; display: grid; grid-template-columns: 1fr 1fr; gap: 8px;">
                <li><i class="fa-solid fa-apple-whole" style="color: #ef4444; width: 20px;"></i> Apple</li>
                <li><i class="fa-solid fa-seedling" style="color: #eab308; width: 20px;"></i> Corn</li>
                <li><i class="fa-solid fa-leaf" style="color: #a855f7; width: 20px;"></i> Grape</li>
                <li><i class="fa-solid fa-lemon" style="color: #fb923c; width: 20px;"></i> Peach</li>
                <li><i class="fa-solid fa-pepper-hot" style="color: #ef4444; width: 20px;"></i> Pepper</li>
                <li><i class="fa-solid fa-carrot" style="color: #d97706; width: 20px;"></i> Potato</li>
                <li><i class="fa-solid fa-leaf" style="color: #f43f5e; width: 20px;"></i> Strawberry</li>
                <li><i class="fa-solid fa-apple-whole" style="color: #ef4444; width: 20px;"></i> Tomato</li>
            </ul>
        </div>
        """,
    )

st.html(
    """
    <div class="glass-card" style="padding: 24px; margin-top: 24px; margin-bottom: 32px;">
        <h3 style="margin-top: 0; color: var(--leaf-primary); font-family: 'Poppins', sans-serif;"><i class="fa-solid fa-viruses"></i> Disease Categories</h3>
        <p style="color: var(--leaf-muted); font-size: 16px; line-height: 1.6; margin: 0;">
            The dataset includes healthy leaves and common disease categories such as
            bacterial spot, early blight, late blight, leaf mold, rust, powdery mildew,
            scab, and leaf scorch.
        </p>
    </div>
    """,
)

# Render floating chatbot globally
chatbot_ui()
