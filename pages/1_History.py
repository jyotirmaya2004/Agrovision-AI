import pandas as pd
import streamlit as st

from frontend.components import page_header, section_title, empty_placeholder
from frontend.styles import load_css
from frontend.ui import require_username, render_navbar
from frontend.sections import load_history, clear_history, _generate_history_pdf
from frontend.chatbot import chatbot_ui


st.set_page_config(
    page_title="Prediction History",
    page_icon=":clipboard:",
    layout="wide",
    initial_sidebar_state="collapsed",
)

load_css()
render_navbar("History")
require_username(force=True)
page_header(
    "Prediction History",
    "Review previous analyses and export them as a PDF or CSV file.",
    "fa-clock-rotate-left",
)

history = load_history()

section_title("Session Records", "fa-table")
if not history:
    empty_placeholder("fa-folder-open", "No History Found", "Analyze a leaf from the Home page first to see records here.")
else:
    df = pd.DataFrame(history)
    st.dataframe(
        df,
        use_container_width=True,
        column_config={
            "Image_URL": st.column_config.ImageColumn("Uploaded Image")
        }
    )

    col1, col2, col3 = st.columns(3)

    pdf_bytes = _generate_history_pdf(history)
    if pdf_bytes:
        with col1:
            if st.download_button(
                label="Download History PDF",
                data=pdf_bytes,
                file_name="plantexa_ai_history.pdf",
                mime="application/pdf",
                use_container_width=True,
            ):
                st.markdown('<div class="success-msg-anim"><i class="fa-solid fa-circle-check"></i> PDF downloaded successfully!</div>', unsafe_allow_html=True)
    with col2:
        if st.download_button(
            "Download CSV",
            df.to_csv(index=False),
            file_name="prediction_history.csv",
            mime="text/csv",
            use_container_width=True,
        ):
            st.markdown('<div class="success-msg-anim"><i class="fa-solid fa-circle-check"></i> CSV downloaded successfully!</div>', unsafe_allow_html=True)
    with col3:
        if st.button("Clear History", use_container_width=True):
            clear_history()
            st.rerun()

# Render floating chatbot globally
chatbot_ui()
