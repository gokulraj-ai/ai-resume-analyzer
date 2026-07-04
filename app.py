"""
AI Interview Preparation Assistant
===================================
Main entry point for the Streamlit application.
Run with: streamlit run app.py
"""

import streamlit as st
from src.ui import render_header, render_sidebar, render_main_content
from src.session import init_session_state

# ── Page configuration ──────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Interview Prep",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Load custom CSS ──────────────────────────────────────────────────────────
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ── Bootstrap session state ──────────────────────────────────────────────────
init_session_state()

# ── Render layout ────────────────────────────────────────────────────────────
render_header()
render_sidebar()
render_main_content()
