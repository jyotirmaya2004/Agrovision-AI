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
        import os
        import json
        from reportlab.lib.pagesizes import letter
        from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
        from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
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

    # Safely attempt to register a custom Unicode font if provided
    base_font = "Helvetica"
    font_path = os.path.join(os.path.dirname(__file__), "..", "assets", "fonts", "UnicodeFont.ttf")
    if os.path.exists(font_path):
        try:
            pdfmetrics.registerFont(TTFont('UnicodeFont', font_path))
            base_font = 'UnicodeFont'
        except Exception:
            pass

    styles.add(ParagraphStyle(name='CustomNormal', parent=styles['Normal'], fontName=base_font, fontSize=11, leading=15))

    # Dynamically load disease data
    disease_names = []
    dynamic_crops = ["Apple", "Corn", "Grape", "Peach", "Pepper", "Potato", "Strawberry", "Tomato"]
    try:
        json_path = os.path.join(os.path.dirname(__file__), "..", "disease_info.json")
        with open(json_path, "r", encoding="utf-8") as f:
            disease_data = json.load(f)
        disease_names = sorted([info.get("disease_name", key.replace("___", " - ").replace("_", " ")) for key, info in disease_data.items()])

        extracted_crops = set()
        for name in disease_names:
            if " - " in name:
                extracted_crops.add(name.split(" - ")[0].strip())
        if extracted_crops:
            dynamic_crops = sorted(list(extracted_crops))
    except Exception:
        pass

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
    story.append(Paragraph("<b>Plantexa AI - Dataset Information</b>", title_style))
    story.append(Spacer(1, 10))

    story.append(Paragraph("<b>Dataset Summary</b>", h2_style))
    story.append(Paragraph("<b>Total classes:</b> 38+", styles["CustomNormal"]))
    story.append(Paragraph("<b>Image format:</b> 224 x 224 (RGB)", styles["CustomNormal"]))
    story.append(Paragraph("<b>Primary purpose:</b> Plant disease identification from leaf images", styles["CustomNormal"]))
    story.append(Paragraph("<b>Source:</b> PlantVillage & Augmented variations", styles["CustomNormal"]))
    story.append(Spacer(1, 10))

    story.append(Paragraph("<b>Extended Details</b>", h2_style))
    story.append(Paragraph("The Plantexa AI dataset is carefully curated from multiple reputable sources, primarily leveraging the widely-used PlantVillage dataset. To ensure robustness, we have augmented the dataset with realistic variations including noise, rotation, and differing lighting conditions. This prepares the model for real-world application across various environments and camera setups.", styles["CustomNormal"]))
    story.append(Spacer(1, 10))

    story.append(Paragraph("<b>Supported Crops</b>", h2_style))
    story.append(Paragraph(", ".join(dynamic_crops), styles["CustomNormal"]))
    story.append(Spacer(1, 10))

    story.append(Paragraph("<b>Disease Categories</b>", h2_style))
    story.append(Paragraph("The dataset encompasses healthy leaves alongside prevalent disease categories such as bacterial spot, early blight, late blight, leaf mold, rust, powdery mildew, scab, and leaf scorch. It is continually updated to include new strains and localized diseases as data becomes available.", styles["CustomNormal"]))

    if disease_names:
        story.append(Spacer(1, 10))
        story.append(Paragraph("<b>Complete List of Classes:</b>", ParagraphStyle(
            'CustomH3', parent=styles['Heading3'], fontName=base_font, fontSize=12, textColor=colors.HexColor('#1b4332'), spaceAfter=8
        )))

        col1, col2 = [], []
        for i, name in enumerate(disease_names):
            if i % 2 == 0: col1.append(name)
            else: col2.append(name)

        if len(col1) > len(col2): col2.append("")

        table_data = []
        for c1, c2 in zip(col1, col2):
            table_data.append([
                Paragraph(f"• {c1}", styles["CustomNormal"]) if c1 else "",
                Paragraph(f"• {c2}", styles["CustomNormal"]) if c2 else ""
            ])

        t = Table(table_data, colWidths=[3.2*inch, 3.2*inch])
        t.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP'), ('BOTTOMPADDING', (0,0), (-1,-1), 4), ('LEFTPADDING', (0,0), (-1,-1), 0)]))
        story.append(t)

    def add_footer(canvas, doc):
        canvas.saveState()
        canvas.setFont(base_font, 9)
        canvas.setFillColor(colors.dimgrey)
        footer_text = f"Plantexa AI Dataset - Page {doc.page}"
        canvas.drawCentredString(letter[0] / 2.0, 0.5 * inch, footer_text)
        date_str = datetime.now(IST).strftime("%B %d, %Y")
        canvas.drawString(0.5 * inch, 0.5 * inch, date_str)
        canvas.restoreState()

    doc.build(story, onFirstPage=add_footer, onLaterPages=add_footer)
    return buffer.getvalue()

pdf_bytes = _generate_dataset_pdf()
col1, col2 = st.columns([1, 2])
with col1:
    if pdf_bytes:
        st.download_button(
            label="Download Dataset PDF",
            data=pdf_bytes,
            file_name="plantexa_dataset.pdf",
            mime="application/pdf",
            use_container_width=True,
        )
    else:
        st.download_button(
            label="Download Dataset PDF",
            data="Please run `pip install reportlab` to enable PDF downloads.",
            file_name="download_error.txt",
            mime="text/plain",
            use_container_width=True,
            help="ReportLab is required for PDF generation."
        )

# Render floating chatbot globally
chatbot_ui()
