import sys
from pathlib import Path

import streamlit as st


st.set_page_config(
    page_title="Plantexa AI",
    page_icon=":seedling:",
    layout="wide",
    initial_sidebar_state="collapsed",
)


ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from frontend.ui import main

active_tab = st.query_params.get("tab", "all")
main(active_tab=active_tab)
