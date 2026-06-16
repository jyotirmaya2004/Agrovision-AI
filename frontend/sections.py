import io
import os
import re
import time
import uuid
from datetime import datetime

import pandas as pd
import streamlit as st
from PIL import Image as PILImage

from backend.disease_info import get_disease_details, _t
from backend.predict_two_stage import PredictionError, predict_two_stage
from frontend.components import (
    empty_placeholder,
    get_confidence_color,
    landing_hero,
    prediction_card,
    section_title,
    top_predictions_card,
)

@st.cache_data(ttl=300, show_spinner=False)
def _fetch_history_cached(user_id):
    from backend.db import fetch_user_history
    rows = fetch_user_history(user_id)
    return [{"Timestamp": r["timestamp"], "Disease": r["disease"], "Confidence": r["confidence"], "Image_URL": r.get("image_url")} for r in rows]

def load_history():
    user_id = st.session_state.get("user_id")
    if not user_id:
        return []
    try:
        return _fetch_history_cached(user_id)
    except Exception as e:
        st.warning(f"Could not load history from Supabase: {e}")
    return []

def append_history(item):
    user_id = st.session_state.get("user_id")
    if not user_id:
        return
    try:
        from backend.db import insert_history_record
        record = {
            "user_id": user_id,
            "timestamp": item["Timestamp"],
            "disease": item["Disease"],
            "confidence": item["Confidence"],
            "image_url": item.get("Image_URL")
        }
        insert_history_record(record)
        _fetch_history_cached.clear()
    except Exception as e:
        st.warning(f"Could not save history to Supabase: {e}")

def clear_history():
    user_id = st.session_state.get("user_id")
    if not user_id:
        return
    try:
        from backend.db import clear_user_history
        clear_user_history(user_id)
        _fetch_history_cached.clear()
    except Exception as e:
        st.warning(f"Could not clear history: {e}")

def render_header():
    landing_hero()


def render_upload_section():
    section_title(_t("Image Input"), "fa-cloud-arrow-up", anchor_id="diagnosis-section")

    col_input, col_preview = st.columns([1.3, 1], gap="large")

    with col_input:
        st.subheader(_t("Choose Input Method"))
        default_source = 1 if st.query_params.get("source") == "camera" else 0
        source_choice = st.radio(
            _t("Select Input Method"),
            [_t("Upload from device"), _t("Use camera")],
            index=default_source,
            horizontal=True,
            label_visibility="collapsed"
        )

        if source_choice in ["Use camera", _t("Use camera")]:
            image_file = st.camera_input(_t("Take a clear leaf photo"), label_visibility="collapsed")
        else:
            image_file = st.file_uploader(
                _t("Choose a leaf image"),
                type=["jpg", "jpeg", "png", "webp", "bmp", "gif", "tiff", "heic", "heif"],
                label_visibility="collapsed"
            )

    with col_preview:
        st.subheader(_t("Analysis Readiness"))
        if image_file:
            st.image(image_file, caption=_t("Ready for analysis"), use_container_width=True)
            size_mb = len(image_file.getvalue()) / (1024 * 1024)
            st.caption(f"**{_t('Status')}:** {_t('Valid File')} | **{_t('File Size')}:** {size_mb:.2f} MB")
        else:
            empty_placeholder("fa-image", _t("No Image Selected"), _t("Your selected image will appear here."))

    return image_file


def _generate_report_pdf(image_bytes, prediction, disease_info):
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
        from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
        from reportlab.platypus import Image as RLImage
        from reportlab.lib import colors
        from reportlab.lib.units import inch
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.ttfonts import TTFont
    except ImportError:
        return None

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

    styles.add(ParagraphStyle(name='TranslatedText', parent=styles['Normal'], fontName=base_font))

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
    story.append(Paragraph("<b>Plantexa AI - Plant Health Report Card</b>", title_style))
    story.append(Spacer(1, 10))

    if image_bytes:
        try:
            img_io = io.BytesIO(image_bytes)
            pil_img = PILImage.open(img_io)
            # Strip transparency channels for flawless PDF insertion
            if pil_img.mode in ('RGBA', 'LA') or (pil_img.mode == 'P' and 'transparency' in pil_img.info):
                alpha = pil_img.convert('RGBA').split()[-1]
                bg = PILImage.new("RGB", pil_img.size, (255, 255, 255))
                bg.paste(pil_img, mask=alpha)
                pil_img = bg
            else:
                pil_img = pil_img.convert('RGB')

            clean_img_io = io.BytesIO()
            pil_img.save(clean_img_io, format='JPEG')
            clean_img_io.seek(0)

            # Proportionally scale image to fit nicely on the document
            img_width, img_height = pil_img.size

            gradcam_b64 = prediction.get("gradcam_b64")
            max_w = 250.0 if gradcam_b64 else 400.0
            max_h = 250.0

            ratio = min(max_w / img_width, max_h / img_height)
            new_w, new_h = img_width * ratio, img_height * ratio

            rl_img = RLImage(clean_img_io, width=new_w, height=new_h)
            img_elements = [rl_img]

            if gradcam_b64:
                import base64
                gc_io = io.BytesIO(base64.b64decode(gradcam_b64))
                gc_img = PILImage.open(gc_io).convert('RGB')
                gc_clean_io = io.BytesIO()
                gc_img.save(gc_clean_io, format='JPEG')
                gc_clean_io.seek(0)
                rl_gc_img = RLImage(gc_clean_io, width=new_w, height=new_h)
                img_elements.append(rl_gc_img)

            img_table = Table([img_elements], colWidths=[new_w + 10] * len(img_elements))
            img_table.setStyle(TableStyle([
                ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e1')),
                ('INNERGRID', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e1')),
                ('TOPPADDING', (0,0), (-1,-1), 5),
                ('BOTTOMPADDING', (0,0), (-1,-1), 5),
                ('LEFTPADDING', (0,0), (-1,-1), 5),
                ('RIGHTPADDING', (0,0), (-1,-1), 5),
            ]))

            if len(img_elements) > 1:
                title_table = Table([
                    [Paragraph("<para align='center'><b>Original Image</b></para>", styles["Normal"]),
                     Paragraph("<para align='center'><b>Grad-CAM Heatmap</b></para>", styles["Normal"])]
                ], colWidths=[new_w + 10, new_w + 10])
                title_table.setStyle(TableStyle([
                    ('BOTTOMPADDING', (0,0), (-1,-1), 2),
                ]))
                story.append(title_table)

            story.append(img_table)
            story.append(Spacer(1, 20))
        except Exception:
            pass

    disease = prediction.get("disease", "Unknown")
    confidence = prediction.get("confidence", 0.0)

    data = [
        [Paragraph("<b>Diagnosed Disease</b>", styles["Normal"]), Paragraph(disease, styles["Normal"])],
        [Paragraph("<b>Model Confidence</b>", styles["Normal"]), Paragraph(f"<font color='{get_confidence_color(confidence)}'><b>{confidence}%</b></font>", styles["Normal"])]
    ]

    top_preds = prediction.get("top_predictions", [])
    if len(top_preds) > 1:
        alts = ", ".join([f"{p['disease']} (<font color='{get_confidence_color(p['confidence'])}'>{p['confidence']}%</font>)" for p in top_preds[1:]])
        data.append([Paragraph("<b>Other Predictions</b>", styles["Normal"]), Paragraph(alts, styles["Normal"])])

    t = Table(data, colWidths=[1.5*inch, 4.5*inch])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,-1), colors.HexColor('#eaf4f0')),
        ('GRID', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e1')),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t)
    story.append(Spacer(1, 15))

    if disease_info:
        for section in ["symptoms", "causes", "treatment", "prevention"]:
            if section in disease_info and disease_info[section]:
                story.append(Paragraph(f"{section.title()}", h2_style))
                text = disease_info[section].replace("<", "&lt;").replace(">", "&gt;")
                story.append(Paragraph(text, styles["TranslatedText"]))
                story.append(Spacer(1, 8))

    def add_footer(canvas, doc):
        canvas.saveState()
        canvas.setFont('Helvetica', 9)
        canvas.setFillColor(colors.dimgrey)
        footer_text = f"Plantexa AI Report Card - Page {doc.page}"
        canvas.drawCentredString(letter[0] / 2.0, 0.5 * inch, footer_text)
        date_str = datetime.now().strftime("%B %d, %Y")
        canvas.drawString(0.5 * inch, 0.5 * inch, date_str)
        canvas.restoreState()

    doc.build(story, onFirstPage=add_footer, onLaterPages=add_footer)
    return buffer.getvalue()


def _generate_history_pdf(history_data):
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
        from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
        from reportlab.platypus import Image as RLImage
        from reportlab.lib import colors
        from reportlab.lib.units import inch
        import httpx
    except ImportError:
        return None

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

    story = []
    story.append(Paragraph("<b>Plantexa AI - Prediction History</b>", title_style))
    story.append(Spacer(1, 10))

    if history_data:
        table_data = [[
            Paragraph("<b>Image</b>", styles["Normal"]),
            Paragraph("<b>Date/Time</b>", styles["Normal"]),
            Paragraph("<b>Disease</b>", styles["Normal"]),
            Paragraph("<b>Confidence</b>", styles["Normal"])
        ]]
        for item in history_data:
            dt = item.get("Timestamp", "N/A")
            disease = item.get("Disease", "Unknown")
            conf_val = item.get("Confidence", 0)
            conf = f"<font color='{get_confidence_color(conf_val)}'><b>{conf_val}%</b></font>"

            img_element = Paragraph("No Image", styles["Normal"])
            img_url = item.get("Image_URL")
            if img_url:
                try:
                    resp = httpx.get(img_url, timeout=5.0)
                    if resp.status_code == 200:
                        img_io = io.BytesIO(resp.content)
                        pil_img = PILImage.open(img_io)

                        if pil_img.mode in ('RGBA', 'LA') or (pil_img.mode == 'P' and 'transparency' in pil_img.info):
                            alpha = pil_img.convert('RGBA').split()[-1]
                            bg = PILImage.new("RGB", pil_img.size, (255, 255, 255))
                            bg.paste(pil_img, mask=alpha)
                            pil_img = bg
                        else:
                            pil_img = pil_img.convert('RGB')

                        clean_img_io = io.BytesIO()
                        pil_img.save(clean_img_io, format='JPEG')
                        clean_img_io.seek(0)

                        img_width, img_height = pil_img.size
                        max_size = 0.9 * inch
                        ratio = min(max_size / img_width, max_size / img_height)
                        img_element = RLImage(clean_img_io, width=img_width * ratio, height=img_height * ratio)
                except Exception:
                    pass

            table_data.append([
                img_element,
                Paragraph(dt, styles["Normal"]),
                Paragraph(disease, styles["Normal"]),
                Paragraph(conf, styles["Normal"])
            ])

        t = Table(table_data, colWidths=[1.2*inch, 1.8*inch, 2.7*inch, 1.3*inch])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#eaf4f0')),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('BOTTOMPADDING', (0,0), (-1,0), 8),
            ('GRID', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e1')),
            ('PADDING', (0,0), (-1,-1), 8),
        ]))
        story.append(t)
    else:
        story.append(Paragraph("No prediction history available.", styles["Normal"]))

    def add_footer(canvas, doc):
        canvas.saveState()
        canvas.setFont('Helvetica', 9)
        canvas.setFillColor(colors.dimgrey)
        footer_text = f"Plantexa AI History - Page {doc.page}"
        canvas.drawCentredString(letter[0] / 2.0, 0.5 * inch, footer_text)
        date_str = datetime.now().strftime("%B %d, %Y")
        canvas.drawString(0.5 * inch, 0.5 * inch, date_str)
        canvas.restoreState()

    doc.build(story, onFirstPage=add_footer, onLaterPages=add_footer)
    return buffer.getvalue()


def render_prediction_section(image_file):
    section_title(_t("Diagnosis Dashboard"), "fa-chart-pie")

    with st.expander(_t("Debug: leaf vs non-leaf output"), expanded=False):
        show_debug = st.checkbox(_t("Show raw leaf validation output"), value=False)

    if image_file is None:
        empty_placeholder("fa-microscope", _t("Awaiting Image"), _t("Please upload or capture an image above to start analysis."))
        return

    st.markdown('<div class="analyze-btn-marker"></div><div class="analyze-btn-spacer"></div>', unsafe_allow_html=True)
    analyze_clicked = st.button(_t("Analyze Leaf"), type="primary", use_container_width=True)

    if analyze_clicked:
        # Require authentication to perform an analysis
        if not st.session_state.get("username"):
            st.session_state.show_auth = True
            st.rerun()

        with st.status(_t("Analyzing Leaf Image..."), expanded=True) as status:
            st.write(_t("☁️ Uploading image to Supabase..."))
            image_url = None
            try:
                from backend.db import upload_image
                file_ext = "jpg"
                if hasattr(image_file, "name") and "." in image_file.name:
                    file_ext = image_file.name.split('.')[-1]
                file_name = f"{uuid.uuid4()}.{file_ext}"
                content_type = image_file.type if hasattr(image_file, "type") else "image/jpeg"
                image_url = upload_image(file_name, image_file.getvalue(), content_type)
            except Exception as e:
                error_msg = str(e).lower()
                if "policy" in error_msg or "row-level security" in error_msg or "unauthorized" in error_msg:
                    st.warning(_t("⚠️ Image upload blocked by Supabase policy restrictions. Please check your storage bucket permissions."))
                else:
                    st.warning(f"Could not upload image to Supabase: {e}")

            try:
                st.write(_t("🔍 Extracting image features..."))
                time.sleep(0.5)
                st.write(_t("🌿 Validating leaf presence..."))
                time.sleep(0.5)
                st.write(_t("🧬 Running disease classification model..."))
                result = predict_two_stage(image_file, top_k=3)

                st.session_state.prediction = result

                new_record = {
                    "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Disease": result["disease"],
                    "Confidence": result["confidence"],
                    "Image_URL": image_url,
                }
                append_history(new_record)

                st.session_state.prediction_history = load_history()
                status.update(label=_t("Analysis Complete"), state="complete", expanded=False)
            except PredictionError as exc:
                st.session_state.prediction = None

                new_record = {
                    "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Disease": "Failed: Invalid Image (Not a Leaf)",
                    "Confidence": 0.0,
                    "Image_URL": image_url,
                }
                append_history(new_record)
                st.session_state.prediction_history = load_history()

                status.update(label=_t("Analysis Failed"), state="error", expanded=False)
                st.error(str(exc))
            except Exception as exc:
                st.session_state.prediction = None

                new_record = {
                    "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Disease": "Analysis Error",
                    "Confidence": 0.0,
                    "Image_URL": image_url,
                }
                append_history(new_record)
                st.session_state.prediction_history = load_history()

                status.update(label=_t("Analysis Failed"), state="error", expanded=False)
                st.error(f"Unexpected error: {exc}")

    result = st.session_state.get("prediction")
    if not result:
        return

    dashboard_container = st.container()
    with dashboard_container:
        st.markdown('<div class="dashboard-slide-up-marker"></div>', unsafe_allow_html=True)

        st.success(_t("Analysis Complete!"))

        if result.get("validation_warning"):
            st.warning(result["validation_warning"])

        # Dashboard Row 1
        col_diag, col_top = st.columns([1, 1], gap="large")
        with col_diag:
            section_title(_t("Diagnosis Result"), "fa-virus")
            prediction_card(result["disease"], result["confidence"])
        with col_top:
            section_title(_t("Alternate Probabilities"), "fa-layer-group")
            top_predictions_card([(pred["disease"], pred["confidence"]) for pred in result["top_predictions"]])

        if show_debug:
            st.json(result["leaf_validation"])

        gradcam_b64 = result.get("gradcam_b64")
        if gradcam_b64:
            st.html("<br>")
            section_title(_t("Explainable AI (Grad-CAM)"), "fa-eye")
            st.info(_t("This heatmap shows the exact regions of the leaf the neural network focused on to make its diagnosis. Warmer colors (red/orange) indicate higher importance."))
            st.html(f"""
            <div style="display: flex; justify-content: center; margin-bottom: 24px;">
                <div class="glass-card" style="padding: 16px; display: inline-block;">
                    <img src="data:image/jpeg;base64,{gradcam_b64}" style="max-width: 100%; max-height: 400px; border-radius: 12px; display: block;">
                </div>
            </div>
            """)

        st.html("<br>")
        section_title(_t("Diagnosis & Treatment Hub"), "fa-briefcase-medical")

        raw_disease_info = get_disease_details(result["class_name"])
        selected_code = st.session_state.get("lang_code", "en")

        if selected_code != "en":
            from backend.disease_info import translate_disease_info
            with st.spinner(_t("Translating guidance...")):
                disease_info = translate_disease_info(raw_disease_info, selected_code)
        else:
            disease_info = raw_disease_info

        tab_sym, tab_treat, tab_prev, tab_comp = st.tabs([_t("Symptoms & Causes"), _t("Treatment Plans"), _t("Prevention"), _t("Similar Diseases")])

        with tab_sym:
            st.write(f"### {_t('Disease Description & Symptoms')}")
            st.write(disease_info.get("symptoms", "No symptom information available."))
            st.write(f"### {_t('Primary Causes')}")
            st.write(disease_info.get("causes", "No cause information available."))

        with tab_treat:
            st.write(f"### {_t('AI Recommended Treatments')}")
            st.info(_t("The following treatments are scientifically recommended based on your diagnosis."))
            st.write(disease_info.get("treatment", "No treatment information available."))
            col_c1, col_c2 = st.columns(2)
            with col_c1:
                st.metric(_t("Estimated Treatment Cost"), _t("Low - Moderate"))
            with col_c2:
                st.metric(_t("Effectiveness Score"), _t("High (85-95%)"))

        with tab_prev:
            st.write(f"### {_t('Best Practices & Prevention')}")
            st.write(disease_info.get("prevention", "No prevention information available."))
            st.success(_t("Follow these practices to prevent future outbreaks and maintain crop health."))

        with tab_comp:
            st.write(f"### {_t('Disease Comparison')}")
            st.write(_t("Comparing current diagnosis against similar pathogens."))
            if len(result["top_predictions"]) > 1:
                alt_disease = result["top_predictions"][1]["disease"]
                st.warning(f"**{_t('Similar Match:')}** {alt_disease}. {_t('Monitor for overlapping symptoms.')}")
            else:
                st.write(_t("No similar diseases found for comparison."))

        st.html("<br>")
        section_title(_t("Diagnosis Report"), "fa-file-pdf")
        st.info(_t("Save a detailed PDF report of this diagnosis, including the uploaded image and treatment guidelines."))

        image_bytes = image_file.getvalue() if image_file else None
        # Now that Unicode fonts are supported, we can safely pass the translated disease_info
        pdf_bytes = _generate_report_pdf(image_bytes, result, disease_info)

        if pdf_bytes:
            safe_name = re.sub(r'[^a-zA-Z0-9]+', '_', result['disease']).strip('_').lower()
            if st.download_button(
                label=_t("Download Full Report Card"),
                data=pdf_bytes,
                file_name=f"plantexa_report_{safe_name}.pdf",
                mime="application/pdf",
            ):
                st.markdown(f'<div class="success-msg-anim"><i class="fa-solid fa-circle-check"></i> {_t("Report downloaded successfully!")}</div>', unsafe_allow_html=True)
        else:
            st.warning("ReportLab is required to generate PDF reports. Please run `pip install reportlab`.")

def render_history_section():
    section_title(_t("Prediction History"), "fa-clock-rotate-left")

    history = load_history()
    st.session_state.prediction_history = history

    if not history:
        st.info(_t("No history yet. Analyze a leaf image to see records here."))
        return

    import pandas as pd

    df = pd.DataFrame(history)

    def color_confidence(val):
        try:
            return f'color: {get_confidence_color(float(val))}'
        except Exception:
            return ''

    # Apply color highlighting across the entire column
    styled_df = df.style.map(color_confidence, subset=['Confidence'])

    st.dataframe(
        styled_df,
        use_container_width=True,
        column_config={
            "Image_URL": st.column_config.ImageColumn(_t("Uploaded Image")),
            "Confidence": st.column_config.NumberColumn(_t("Confidence"), format="%.2f%%")
        }
    )

    col1, col2 = st.columns(2)

    pdf_bytes = _generate_history_pdf(history)
    if pdf_bytes:
        with col1:
            if st.download_button(
                label=_t("Download History PDF"),
                data=pdf_bytes,
                file_name="plantexa_ai_history.pdf",
                mime="application/pdf",
                use_container_width=True,
            ):
                st.markdown(f'<div class="success-msg-anim"><i class="fa-solid fa-circle-check"></i> {_t("PDF downloaded successfully!")}</div>', unsafe_allow_html=True)
    with col2:
        if st.button(_t("Clear History"), key="clear_history_home", use_container_width=True):
            clear_history()
            st.session_state.prediction_history = []
            st.rerun()


def render_tips_section():
    section_title(_t("Quick Care Tips"), "fa-lightbulb")

    st.html("""
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 16px; margin-bottom: 24px;">
        <div class="glass-card staggered-slide-up" style="padding: 20px; border-top: 3px solid #3b82f6; animation-delay: 0s;">
            <h4 style="margin-top:0; color: #60a5fa; font-family: 'Poppins', sans-serif;"><i class="fa-solid fa-droplet"></i> {_t('Watering')}</h4>
            <p style="color: var(--leaf-muted); font-size: 14px; margin-bottom: 0;">{_t('Water at the base of the plant to prevent leaf wetness and fungal growth.')}</p>
        </div>
        <div class="glass-card staggered-slide-up" style="padding: 20px; border-top: 3px solid #eab308; animation-delay: 0.15s;">
            <h4 style="margin-top:0; color: #fde047; font-family: 'Poppins', sans-serif;"><i class="fa-solid fa-sun"></i> {_t('Sunlight')}</h4>
            <p style="color: var(--leaf-muted); font-size: 14px; margin-bottom: 0;">{_t('Ensure proper canopy pruning to allow UV light to naturally disinfect lower leaves.')}</p>
        </div>
        <div class="glass-card staggered-slide-up" style="padding: 20px; border-top: 3px solid #a855f7; animation-delay: 0.3s;">
            <h4 style="margin-top:0; color: #c084fc; font-family: 'Poppins', sans-serif;"><i class="fa-solid fa-wind"></i> {_t('Airflow')}</h4>
            <p style="color: var(--leaf-muted); font-size: 14px; margin-bottom: 0;">{_t('Maintain adequate spacing between crops to reduce humidity and powdery mildew risk.')}</p>
        </div>
    </div>
    """)


def render_footer():
    st.html(f"""
    <div class="saas-footer">
        <div class="footer-gradient-line"></div>

        <!-- Floating Particles -->
        <div class="footer-particle fp-1"></div>
        <div class="footer-particle fp-2"></div>
        <div class="footer-particle fp-3"></div>
        <div class="footer-particle fp-4"></div>

        <div class="footer-content">
            <!-- Statistics Bar -->
            <div class="footer-stats">
                <div class="f-stat"><span class="f-stat-val">15+</span><span class="f-stat-label">{_t('Plant Species')}</span></div>
                <div class="f-stat"><span class="f-stat-val">38+</span><span class="f-stat-label">{_t('Diseases')}</span></div>
                <div class="f-stat"><span class="f-stat-val">98%</span><span class="f-stat-label">{_t('Accuracy')}</span></div>
                <div class="f-stat"><span class="f-stat-val">10K+</span><span class="f-stat-label">{_t('Analyses')}</span></div>
            </div>

            <!-- Trust Indicators -->
            <div class="footer-trust">
                <span><i class="fa-solid fa-check"></i> {_t('AI Powered')}</span>
                <span><i class="fa-solid fa-check"></i> {_t('NVIDIA Accelerated')}</span>
                <span><i class="fa-solid fa-check"></i> {_t('Secure Uploads')}</span>
                <span><i class="fa-solid fa-check"></i> {_t('Real-Time Analysis')}</span>
                <span><i class="fa-solid fa-check"></i> {_t('Research Grade Models')}</span>
            </div>

            <!-- Main Columns -->
            <div class="footer-grid">
                <!-- Column 1: Brand -->
                <div class="footer-col">
                    <div class="f-logo">
                        <i class="fa-solid fa-leaf f-logo-icon"></i> Plantexa AI
                    </div>
                    <p class="f-desc">{_t('AI-powered plant disease diagnosis and crop health intelligence platform.')}</p>
                    <div class="f-badges">
                        <span class="f-badge">v2.0.0</span>
                        <span class="f-badge nvidia-badge"><i class="fa-solid fa-microchip"></i> {_t('Powered by NVIDIA AI')}</span>
                    </div>
                </div>

                <!-- Column 2: Navigation -->
                <div class="footer-col">
                    <h4 class="f-heading">{_t('Navigation')}</h4>
                    <a href="#diagnosis-section" class="f-link">{_t('Home')}</a>
                    <a href="#diagnosis-section" class="f-link">{_t('Disease Detection')}</a>
                    <a href="?tab=history" class="f-link">{_t('Prediction History')}</a>
                    <a href="?tab=history" class="f-link">{_t('Reports')}</a>
                    <a href="#diagnosis-section" class="f-link">{_t('Dashboard')}</a>
                    <a href="#diagnosis-section" class="f-link">{_t('Analytics')}</a>
                    <a href="?tab=chat" class="f-link">{_t('Chat Assistant')}</a>
                </div>

                <!-- Column 3: Resources -->
                <div class="footer-col">
                    <h4 class="f-heading">{_t('Resources')}</h4>
                    <a href="#" class="f-link">{_t('Documentation')}</a>
                    <a href="#" class="f-link">{_t('User Guide')}</a>
                    <a href="#" class="f-link">FAQ</a>
                    <a href="#" class="f-link">{_t('API Reference')}</a>
                    <a href="#" class="f-link">{_t('Privacy Policy')}</a>
                    <a href="#" class="f-link">{_t('Terms & Conditions')}</a>
                </div>

                <!-- Column 4: Contact & Newsletter -->
                <div class="footer-col">
                    <h4 class="f-heading">{_t('Connect')}</h4>
                    <a href="#" class="f-social"><i class="fa-brands fa-github"></i> GitHub</a>
                    <a href="#" class="f-social"><i class="fa-brands fa-linkedin"></i> LinkedIn</a>
                    <a href="#" class="f-social"><i class="fa-solid fa-envelope"></i> {_t('Email')}</a>
                    <a href="#" class="f-social"><i class="fa-solid fa-briefcase"></i> {_t('Portfolio')}</a>
                    <a href="#" class="f-social"><i class="fa-solid fa-headset"></i> {_t('Contact Us')}</a>

                    <div style="margin-top: 24px;">
                        <p class="f-desc" style="margin-bottom: 8px;">{_t('Get latest crop disease updates')}</p>
                        <form class="f-form" onsubmit="event.preventDefault();">
                            <input type="email" placeholder="{_t('Email address...')}" class="f-input" />
                            <button type="submit" class="f-submit"><i class="fa-solid fa-arrow-right"></i></button>
                        </form>
                    </div>
                </div>
            </div>

            <!-- Bottom Copyright Section -->
            <div class="footer-bottom">
                <p>&copy; 2026 Plantexa AI</p>
                <p>{_t('Built with Streamlit')} <i class="fa-solid fa-plus" style="font-size:10px; margin:0 4px; color:var(--leaf-primary);"></i> {_t('Deep Learning')} <i class="fa-solid fa-plus" style="font-size:10px; margin:0 4px; color:var(--leaf-primary);"></i> NVIDIA AI</p>
            </div>
        </div>
    </div>
    """)