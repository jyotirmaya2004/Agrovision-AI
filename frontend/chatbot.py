import io
import os
import re

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI


NVIDIA_BASE_URL = "https://integrate.api.nvidia.com/v1"
DEFAULT_MODEL = "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning"
SYSTEM_PROMPT = """
You are Plantexa AI, a professional agronomist and plant pathologist.
Provide expert, scientifically accurate advice on plant diseases, crop care, fertilizers, and pest management.
Keep your responses extremely concise, using short bullet points and direct, actionable recommendations.
If the user asks about topics outside of agriculture or botany, politely decline and steer the conversation back to plant health.
""".strip()

AVATAR_ROLES = {
    "🧑‍🌾": "Farmer",
    "👩‍🌾": "Gardener",
    "👨‍🌾": "Agronomist",
    "🪴": "Plant Lover",
    "🌻": "Sunflower",
    "🌵": "Cactus",
    "🌾": "Botanist",
    "🤖": "AI Bot"
}


def _get_float_env(name: str, default: float) -> float:
    try:
        return float(os.getenv(name, default))
    except (TypeError, ValueError):
        return default


def _get_int_env(name: str, default: int) -> int:
    try:
        return int(os.getenv(name, default))
    except (TypeError, ValueError):
        return default


def reset_chat():
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hello! Ask me about leaf diseases, crop care, pests, fertilizers, or treatment steps.",
        }
    ]
    st.session_state.followups = [
        "How to identify leaf diseases?",
        "What are common pests?",
        "How to improve soil health?",
    ]


def initialize_chat():
    load_dotenv()

    if "messages" not in st.session_state:
        reset_chat()

    if "chat_open" not in st.session_state:
        st.session_state.chat_open = False

    if "followups" not in st.session_state:
        st.session_state.followups = [
            "How to identify leaf diseases?",
            "What are common pests?",
            "How to improve soil health?",
        ]


def _build_client() -> OpenAI | None:
    api_key = os.getenv("NVIDIA_API_KEY")
    if not api_key:
        return None

    return OpenAI(
        api_key=api_key,
        base_url=NVIDIA_BASE_URL,
    )


def _chat_with_nvidia_stream():
    client = _build_client()
    if client is None:
        yield "NVIDIA_API_KEY is missing. Add it to your .env file and restart Streamlit."
        return

    system_prompt = SYSTEM_PROMPT

    username = st.session_state.get("username")
    avatar = st.session_state.get("avatar")
    if username:
        role = AVATAR_ROLES.get(avatar, "Plant Enthusiast")
        system_prompt += f"\n\nUser Context: You are talking to {username}, whose profile indicates they are a {role} (Avatar: {avatar}). Personalize your greetings and tailor your advice to match their experience level and perspective when appropriate."

    prediction = st.session_state.get("prediction")
    if prediction and prediction.get("disease"):
        disease = prediction["disease"]
        confidence = prediction.get("confidence", 0)

        try:
            conf_val = float(confidence)
        except (ValueError, TypeError):
            conf_val = 0.0

        if conf_val >= 90:
            st_color = "green"
        elif conf_val >= 70:
            st_color = "orange"
        else:
            st_color = "red"

        system_prompt += (
            f"\n\nCurrent Context: The user just analyzed a plant leaf. "
            f"The AI model diagnosed it as '{disease}' with {confidence}% confidence. "
            f"Tailor your advice to this context if the user's question is ambiguous. "
            f"IMPORTANT: Whenever you mention the confidence percentage, wrap it exactly in this markdown format: :{st_color}[{confidence}%]"
        )

    messages = [{"role": "system", "content": system_prompt}]
    messages.extend(
        {
            "role": message["role"],
            "content": message["content"],
        }
        for message in st.session_state.messages
        if message["role"] in {"user", "assistant"}
    )

    response = client.chat.completions.create(
        model=os.getenv("NVIDIA_MODEL", DEFAULT_MODEL),
        messages=messages,
        temperature=_get_float_env("NVIDIA_TEMPERATURE", 0.6),
        top_p=_get_float_env("NVIDIA_TOP_P", 0.95),
        max_tokens=_get_int_env("NVIDIA_MAX_TOKENS", 1200),
        stream=True,
    )

    for chunk in response:
        if chunk.choices and chunk.choices[0].delta.content is not None:
            yield chunk.choices[0].delta.content


def _generate_followups(messages) -> list[str]:
    client = _build_client()
    if not client:
        return []

    sys_prompt = "Suggest exactly 3 short follow-up questions for the user based on the conversation. Output them strictly on a single line separated by a pipe character `|`. Do not include any intro text, numbers, or bullet points."

    prediction = st.session_state.get("prediction")
    if prediction and prediction.get("disease"):
        sys_prompt += f" The user's plant was just diagnosed with '{prediction['disease']}'."

    context = [m for m in messages if m["role"] in {"user", "assistant"}][-4:]
    api_messages = [{"role": "system", "content": sys_prompt}] + context

    try:
        response = client.chat.completions.create(
            model=os.getenv("NVIDIA_MODEL", DEFAULT_MODEL),
            messages=api_messages,
            temperature=0.7,
            max_tokens=80,
        )
        text = response.choices[0].message.content.strip()
        text = text.replace("`", "")
        questions = [q.strip() for q in text.split('|') if q.strip()]
        return questions[:3]
    except Exception:
        return []


def _render_message_bubbles():
    for message in st.session_state.messages:
        role = "user" if message["role"] == "user" else "assistant"

        with st.chat_message(role):
            if role == "user":
                st.markdown('<div class="user-msg-marker"></div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="assistant-msg-marker"></div>', unsafe_allow_html=True)
            st.markdown(message["content"])


def _generate_pdf_transcript(messages):
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
        from reportlab.lib import colors
        from reportlab.lib.units import inch
        from datetime import datetime
    except ImportError:
        return None

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40,
    )
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("Plantexa AI - Chat Transcript", styles["Title"]))
    story.append(Spacer(1, 20))

    def format_text(text):
        text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        # Restore explicit <br> tags used by the LLM in table cells
        text = text.replace("&lt;br&gt;", "<br/>").replace("&lt;br/&gt;", "<br/>")
        # Parse basic markdown bold and italic formatting
        text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
        text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)
        # Parse markdown headings (##, ###, ####) and convert to bold text
        text = re.sub(r'(?m)^#{1,6}\s+(.*)', r'<b>\1</b>', text)

        # Parse Streamlit color tags to ReportLab font tags
        text = re.sub(r':green\[(.*?)\]', r'<font color="#22c55e">\1</font>', text)
        text = re.sub(r':orange\[(.*?)\]', r'<font color="#fbbf24">\1</font>', text)
        text = re.sub(r':red\[(.*?)\]', r'<font color="#ef4444">\1</font>', text)

        # Strip emojis and unsupported symbols to prevent PDF rendering errors/black boxes
        text = re.sub(r'[^\x00-\x7F\u0080-\u00FF\u2013\u2014\u2018-\u201D\u2022]', '', text)
        return text

    for msg in messages:
        is_user = msg["role"] == "user"

        role_name = 'User' if is_user else 'Plantexa AI'
        color = '#1b4332' if is_user else '#2d6a4f'

        role_html = f'<font color="{color}"><b>{role_name}:</b></font>'
        story.append(Paragraph(role_html, styles["Heading4"]))
        story.append(Spacer(1, 6))

        blocks = []
        current_block = []
        in_table = False

        for line in msg["content"].split('\n'):
            stripped = line.strip()
            # Detect markdown table rows
            if stripped.startswith('|') and stripped.endswith('|') and stripped.count('|') >= 2:
                if not in_table:
                    if current_block:
                        blocks.append(('text', '\n'.join(current_block)))
                        current_block = []
                    in_table = True
                current_block.append(stripped)
            else:
                if in_table:
                    blocks.append(('table', current_block))
                    current_block = []
                    in_table = False
                current_block.append(line)

        if current_block:
            if in_table:
                blocks.append(('table', current_block))
            else:
                blocks.append(('text', '\n'.join(current_block)))

        for block_type, content in blocks:
            if block_type == 'text':
                text_content = format_text(content).replace('\n', '<br/>')
                if text_content.strip():
                    story.append(Paragraph(text_content, styles["Normal"]))
                    story.append(Spacer(1, 8))
            elif block_type == 'table':
                raw_rows = []
                max_cols = 0
                for row_line in content:
                    # Skip the markdown separator row (e.g., |---|---|)
                    if re.match(r'^\|[-\s:|]+\|$', row_line.strip()):
                        continue
                    row_cells = [cell.strip() for cell in row_line.strip().strip('|').split('|')]
                    max_cols = max(max_cols, len(row_cells))
                    raw_rows.append(row_cells)

                if raw_rows and max_cols > 0:
                    formatted_table_data = []
                    for row in raw_rows:
                        # Pad missing columns with empty strings to prevent alignment crashes
                        padded_row = row + [""] * (max_cols - len(row))
                        formatted_cells = [Paragraph(format_text(cell) or "&nbsp;", styles["Normal"]) for cell in padded_row]
                        formatted_table_data.append(formatted_cells)

                    # Calculate equal widths based on standard letter page size (612pt width - 80pt margins = 532pt)
                    col_widths = [532.0 / max_cols] * max_cols
                    t = Table(formatted_table_data, colWidths=col_widths)
                    t.setStyle(TableStyle([
                        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
                        ('TEXTCOLOR', (0,0), (-1,0), colors.black),
                        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
                        ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                        ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                        ('VALIGN', (0,0), (-1,-1), 'TOP'),
                        ('TOPPADDING', (0,0), (-1,-1), 6),
                        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
                    ]))
                    story.append(t)
                    story.append(Spacer(1, 8))

        # Draw a clean separator line between chat messages
        story.append(Spacer(1, 8))
        hr = Table([['']], colWidths=[532.0])
        hr.setStyle(TableStyle([
            ('LINEABOVE', (0,0), (-1,-1), 0.5, colors.lightgrey),
            ('TOPPADDING', (0,0), (-1,-1), 0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 0)
        ]))
        story.append(hr)
        story.append(Spacer(1, 16))

    def add_footer(canvas, doc):
        canvas.saveState()
        canvas.setFont('Helvetica', 9)
        canvas.setFillColor(colors.dimgrey)
        footer_text = f"Plantexa AI Chat Transcript - Page {doc.page}"
        canvas.drawCentredString(letter[0] / 2.0, 0.5 * inch, footer_text)
        date_str = datetime.now().strftime("%B %d, %Y")
        canvas.drawString(0.5 * inch, 0.5 * inch, date_str)
        canvas.restoreState()

    doc.build(story, onFirstPage=add_footer, onLaterPages=add_footer)
    return buffer.getvalue()


def chatbot_ui():
    initialize_chat()

    if not st.session_state.get("chat_open"):
        # Floating UI: Native Streamlit button styled as a FAB via CSS
        fab_container = st.container()
        with fab_container:
            st.markdown('<div class="chat-fab-marker"></div>', unsafe_allow_html=True)
            if st.button("Open Chat", key="open_chat", help="Open Plantexa AI chat"):
                st.session_state.chat_open = True
                st.rerun()
        return

    chat_container = st.container()
    with chat_container:
        # Hidden marker to anchor the CSS targeting using the :has() selector
        st.markdown('<div class="chat-floating-panel-marker"></div>', unsafe_allow_html=True)

        col_title, col_download, col_clear, col_close = st.columns([5, 1, 1, 1])
        with col_title:
            st.html('<div class="chat-title" style="margin-top: 8px;"><i class="fa-solid fa-robot"></i> Plantexa AI Assistant</div>')
        with col_download:
            # Download chat history
            st.markdown('<div class="chat-btn-download-marker"></div>', unsafe_allow_html=True)
            pdf_bytes = _generate_pdf_transcript(st.session_state.messages)

            prediction = st.session_state.get("prediction")
            pdf_filename = "plantexa_ai_chat_transcript.pdf"
            if prediction and prediction.get("disease"):
                safe_name = re.sub(r'[^a-zA-Z0-9]+', '_', prediction["disease"]).strip('_').lower()
                pdf_filename = f"plantexa_ai_{safe_name}_transcript.pdf"

            if pdf_bytes:
                st.download_button(
                    label="Download",
                    data=pdf_bytes,
                    file_name=pdf_filename,
                    mime="application/pdf",
                    key="download_chat",
                    help="Download chat as PDF",
                    use_container_width=False,
                )
            else:
                st.download_button(
                    label="Download",
                    data="Please run `pip install reportlab` in your terminal to enable PDF downloads.",
                    file_name="download_error.txt",
                    mime="text/plain",
                    key="download_chat",
                    help="ReportLab is required for PDF downloads",
                    use_container_width=False,
                )
        with col_clear:
            # Clear chat history
            st.markdown('<div class="chat-btn-clear-marker"></div>', unsafe_allow_html=True)
            if st.button("Clear", key="clear_chat", help="Clear chat", use_container_width=False):
                reset_chat()
                st.rerun()
        with col_close:
            # Close chat panel
            st.markdown('<div class="chat-btn-close-marker"></div>', unsafe_allow_html=True)
            if st.button("Close", key="close_chat", help="Close chat", use_container_width=False):
                st.session_state.chat_open = False
                st.rerun()

        # Fixed height container handles chat scrolling naturally in Streamlit
        messages_container = st.container(height=350)
        with messages_container:
            _render_message_bubbles()
            followups_placeholder = st.container()

        selected_followup = None
        if st.session_state.get("followups"):
            with followups_placeholder:
                followups = st.session_state.followups[:3]
                cols = st.columns(len(followups))
                for i, q in enumerate(followups):
                    with cols[i]:
                        if i == 0:
                            st.markdown('<div class="chat-followup-marker"></div>', unsafe_allow_html=True)
                        if st.button(q, key=f"fw_{i}_{q}", use_container_width=True):
                            selected_followup = q

        with st.form("floating_chat_form", clear_on_submit=True):
            col_input, col_send = st.columns([5, 1])
            with col_input:
                prompt = st.text_input(
                    "Message",
                    placeholder="Ask about leaf disease treatment...",
                    label_visibility="collapsed",
                )
            with col_send:
                st.markdown('<div class="chat-btn-send-marker"></div>', unsafe_allow_html=True)
                submitted = st.form_submit_button("Send", use_container_width=True)

        final_prompt = selected_followup or (prompt.strip() if submitted else None)

        if final_prompt:
            followups_placeholder.empty()
            st.session_state.messages.append({"role": "user", "content": final_prompt})

            with messages_container:
                # Render the user's message immediately
                with st.chat_message("user"):
                    st.markdown('<div class="user-msg-marker"></div>', unsafe_allow_html=True)
                    st.markdown(final_prompt)

                # Render the assistant's response via stream
                with st.chat_message("assistant"):
                    st.markdown('<div class="assistant-msg-marker"></div>', unsafe_allow_html=True)

                    loader_placeholder = st.empty()
                    with loader_placeholder:
                        st.markdown('<div class="chat-thinking"><i class="fa-solid fa-circle-notch fa-spin"></i> Thinking...</div>', unsafe_allow_html=True)

                    try:
                        stream = _chat_with_nvidia_stream()

                        def stream_with_loader():
                            started = False
                            for chunk in stream:
                                if not started:
                                    loader_placeholder.empty()  # Clear loader on the first character
                                    started = True
                                yield chunk

                        response = st.write_stream(stream_with_loader())
                    except Exception as exc:
                        loader_placeholder.empty()
                        response = f"Chat API error: {exc}"
                        st.write(response)

            st.session_state.messages.append({"role": "assistant", "content": response})
            st.session_state.followups = _generate_followups(st.session_state.messages)
            st.rerun()
