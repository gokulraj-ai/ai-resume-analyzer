"""
session.py — Streamlit session state management.
All app-wide state lives here so every module can read/write it consistently.
"""

import streamlit as st


def init_session_state() -> None:
    """Initialise every session-state key exactly once (idempotent)."""

    defaults = {
        # ── Question state ───────────────────────────────────────────────────
        "current_question": None,       # str  – the generated question text
        "question_topic": None,         # str  – topic the question belongs to
        "question_difficulty": None,    # str  – difficulty level selected

        # ── Answer & feedback state ──────────────────────────────────────────
        "user_answer": "",              # str  – what the user typed
        "feedback": None,               # dict – structured feedback from AI
        "evaluation_done": False,       # bool – True after evaluation runs

        # ── History ─────────────────────────────────────────────────────────
        "history": [],                  # list[dict] – past Q&A records

        # ── UI flags ─────────────────────────────────────────────────────────
        "generating": False,            # True while waiting for a question
        "evaluating": False,            # True while waiting for evaluation
        "api_key_valid": False,         # True once key passes a basic check
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
