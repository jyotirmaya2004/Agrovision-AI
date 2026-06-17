import io
import streamlit as st
from datetime import datetime, timezone, timedelta

from frontend.components import page_header, section_title
from frontend.styles import load_css
from frontend.ui import render_navbar
from frontend.chatbot import chatbot_ui


st.set_page_config(
    page_title="Dataset Information",
    page_icon=":books:",
    layout="wide",
    initial_sidebar_state="collapsed",
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

def _generate_dataset_pdf():
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
        from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer
        from reportlab.lib import colors
        from reportlab.lib.units import inch
    except ImportError:
        return None

    IST = timezone(timedelta(hours=5, minutes=30))
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40
    )
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Title'],
        fontSize=22,
        textColor=colors.HexColor('#1b4332'),
        spaceAfter=20
    )

    h2_style = ParagraphStyle(
        'CustomH2',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#2d6a4f'),
        spaceBefore=12,
        spaceAfter=6
    )

    story = []
    story.append(Paragraph("<b>Plantexa AI - Dataset Information</b>", title_style))
    story.append(Spacer(1, 10))

    story.append(Paragraph("<b>Dataset Summary</b>", h2_style))
    story.append(Paragraph("<b>Total classes:</b> 38+", styles["Normal"]))
    story.append(Paragraph("<b>Image format:</b> 224 x 224 (RGB)", styles["Normal"]))
    story.append(Paragraph("<b>Primary purpose:</b> Plant disease identification from leaf images", styles["Normal"]))
    story.append(Paragraph("<b>Source:</b> PlantVillage & Augmented variations", styles["Normal"]))
    story.append(Spacer(1, 10))

    story.append(Paragraph("<b>Supported Crops</b>", h2_style))
    crops = ["Apple", "Corn", "Grape", "Peach", "Pepper", "Potato", "Strawberry", "Tomato"]
    story.append(Paragraph(", ".join(crops), styles["Normal"]))
    story.append(Spacer(1, 10))

    story.append(Paragraph("<b>Disease Categories</b>", h2_style))
    story.append(Paragraph("The dataset includes healthy leaves and common disease categories such as bacterial spot, early blight, late blight, leaf mold, rust, powdery mildew, scab, and leaf scorch.", styles["Normal"]))

    def add_footer(canvas, doc):
        canvas.saveState()
        canvas.setFont('Helvetica', 9)
        canvas.setFillColor(colors.dimgrey)
        footer_text = f"Plantexa AI Dataset - Page {doc.page}"
        canvas.drawCentredString(letter[0] / 2.0, 0.5 * inch, footer_text)
        date_str = datetime.now(IST).strftime("%B %d, %Y")
        canvas.drawString(0.5 * inch, 0.5 * inch, date_str)
        canvas.restoreState()

    doc.build(story, onFirstPage=add_footer, onLaterPages=add_footer)
    return buffer.getvalue()

pdf_bytes = _generate_dataset_pdf()
if pdf_bytes:
    col1, col2 = st.columns([1, 2])
    with col1:
        st.download_button(
            label="Download Dataset PDF",
            data=pdf_bytes,
            file_name="plantexa_dataset.pdf",
            mime="application/pdf",
            use_container_width=True,
        )

# Render floating chatbot globally
chatbot_ui()
