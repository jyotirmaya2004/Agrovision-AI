import io
import os
import streamlit as st
from datetime import datetime, timezone, timedelta

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

def _generate_about_pdf():
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
        from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle, Image as RLImage
        from reportlab.lib import colors
        from reportlab.lib.units import inch
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.ttfonts import TTFont
    except ImportError:
        return None

    IST = timezone(timedelta(hours=5, minutes=30))
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40
    )
    styles = getSampleStyleSheet()

    base_font = "Helvetica"
    font_path = os.path.join(os.path.dirname(__file__), "..", "assets", "fonts", "UnicodeFont.ttf")
    if os.path.exists(font_path):
        try:
            pdfmetrics.registerFont(TTFont('UnicodeFont', font_path))
            base_font = 'UnicodeFont'
        except Exception:
            pass

    styles.add(ParagraphStyle(name='CustomNormal', parent=styles['Normal'], fontName=base_font, fontSize=11, leading=15))

    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Title'],
        fontName=base_font,
        fontSize=22,
        textColor=colors.HexColor('#1b4332'),
        spaceAfter=20
    )

    h2_style = ParagraphStyle(
        'CustomH2',
        parent=styles['Heading2'],
        fontName=base_font,
        fontSize=14,
        textColor=colors.HexColor('#2d6a4f'),
        spaceBefore=12,
        spaceAfter=6
    )

    story = []
    story.append(Paragraph("<b>Plantexa AI - About Project</b>", title_style))
    story.append(Spacer(1, 10))

    story.append(Paragraph("<b>Project Overview</b>", h2_style))
    story.append(Paragraph("Plantexa AI uses a two-stage deep learning workflow. It first checks whether the uploaded image looks like a plant leaf, then predicts the most likely disease and shows symptoms, causes, treatment, and prevention guidance from the disease knowledge base.", styles["CustomNormal"]))
    story.append(Spacer(1, 10))

    story.append(Paragraph("<b>Features</b>", h2_style))
    story.append(Paragraph("• Two-Stage Pipeline: Leaf detection before disease classification<br/>• AI Analysis: Top 3 predictions with real-time confidence scores<br/>• Knowledge Base: Detailed disease symptoms, causes, treatment, and prevention<br/>• NVIDIA LLM: Context-aware AI agriculture assistant<br/>• Reporting: Downloadable PDF report cards and session prediction history", styles["CustomNormal"]))
    story.append(Spacer(1, 10))

    story.append(Paragraph("<b>Meet the Team</b>", h2_style))

    team_members = [
        {"name": "Jyotirmaya Behera", "id": "3146/24", "role": "AI Engineer", "contribution": "AI Models & Core Logic", "img_prefix": "jyotirmaya"},
        {"name": "Diptesh Ranjan Pradhan", "id": "3141/24", "role": "Backend Developer", "contribution": "Database & Supabase API", "img_prefix": "diptesh"},
        {"name": "Bibekananda Sahoo", "id": "3136/24", "role": "UI/UX Designer", "contribution": "Glassmorphism UI/UX Design", "img_prefix": "bibekananda"},
        {"name": "Pritam Kumar Behera", "id": "3159/24", "role": "Frontend Developer", "contribution": "Streamlit Frontend & Logic", "img_prefix": "pritam"},
        {"name": "Laxman Kumar Sahoo", "id": "3148/24", "role": "Data Scientist", "contribution": "Data Collection & Preprocessing", "img_prefix": "laxman"}
    ]

    for member in team_members:
        img_path = ""
        for ext in ['jpg', 'png', 'webp']:
            p = os.path.join(os.path.dirname(__file__), "..", "assets", f"{member['img_prefix']}.{ext}")
            if os.path.exists(p):
                img_path = p
                break

        member_info = f"<b>{member['name']}</b> (ID: {member['id']})<br/><b>Role:</b> {member['role']}<br/><b>Contribution:</b> {member['contribution']}"

        row_data = []
        if img_path:
            try:
                from PIL import Image as PILImage
                pil_img = PILImage.open(img_path).convert('RGB')
                clean_img_io = io.BytesIO()
                pil_img.save(clean_img_io, format='JPEG')
                clean_img_io.seek(0)
                img_width, img_height = pil_img.size
                max_size = 1.2 * inch
                ratio = min(max_size / img_width, max_size / img_height)
                rl_img = RLImage(clean_img_io, width=img_width * ratio, height=img_height * ratio)
                row_data.append(rl_img)
            except Exception:
                row_data.append(Paragraph("No Image", styles["CustomNormal"]))
        else:
            row_data.append(Paragraph("No Image", styles["CustomNormal"]))

        row_data.append(Paragraph(member_info, styles["CustomNormal"]))

        t = Table([row_data], colWidths=[1.5*inch, 4.5*inch])
        t.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ]))
        story.append(t)
        story.append(Spacer(1, 5))

    def add_footer(canvas, doc):
        canvas.saveState()
        canvas.setFont(base_font, 9)
        canvas.setFillColor(colors.dimgrey)
        footer_text = f"Plantexa AI About - Page {doc.page}"
        canvas.drawCentredString(letter[0] / 2.0, 0.5 * inch, footer_text)
        date_str = datetime.now(IST).strftime("%B %d, %Y")
        canvas.drawString(0.5 * inch, 0.5 * inch, date_str)
        canvas.restoreState()

    doc.build(story, onFirstPage=add_footer, onLaterPages=add_footer)
    return buffer.getvalue()

pdf_bytes = _generate_about_pdf()
col1, col2 = st.columns([1, 2])
with col1:
    if pdf_bytes:
        st.download_button(
            label="Download About PDF",
            data=pdf_bytes,
            file_name="plantexa_about.pdf",
            mime="application/pdf",
            use_container_width=True,
        )
    else:
        st.download_button(
            label="Download About PDF",
            data="Please run `pip install reportlab` to enable PDF downloads.",
            file_name="download_error.txt",
            mime="text/plain",
            use_container_width=True,
            help="ReportLab is required for PDF generation."
        )

# Render floating chatbot globally
chatbot_ui()
