"""
ui.py — Every Streamlit rendering function for the app.

Structure:
  render_header()        → top banner
  render_sidebar()       → API key + topic/difficulty pickers
  render_main_content()  → question panel + answer area + feedback
  _render_feedback()     → score card + detailed feedback panels
  _render_history()      → collapsible past Q&A accordion
"""

import streamlit as st

from src.config import (
    TOPICS, DIFFICULTIES, DIFFICULTY_META,
    SCORE_COLOURS, APP_TITLE, APP_TAGLINE,
)
from src.gemini import configure_api, generate_question, evaluate_answer


# ─────────────────────────────────────────────────────────────────────────────
# Header
# ─────────────────────────────────────────────────────────────────────────────

def render_header() -> None:
    """Render the top-of-page banner."""
    st.markdown(
        f"""
        <div class="app-header">
            <h1>🎯 {APP_TITLE}</h1>
            <p class="tagline">{APP_TAGLINE}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────────────────────────────────────
# Sidebar
# ─────────────────────────────────────────────────────────────────────────────

def render_sidebar() -> None:
    """Render the left sidebar: API key input + topic & difficulty selection."""
    with st.sidebar:
        st.markdown("## ⚙️ Settings")
        st.divider()

        # ── API Key ───────────────────────────────────────────────────────────
        st.markdown("### 🔑 Gemini API Key")
        api_key = st.text_input(
            "Enter your key",
            type="password",
            placeholder="AIza...",
            help="Get a free key at https://aistudio.google.com/app/apikey",
            label_visibility="collapsed",
        )

        if api_key:
            try:
                configure_api(api_key)
                st.session_state.api_key_valid = True
                st.session_state.api_key = api_key
                st.success("✅ API key saved", icon="✅")
            except ValueError as exc:
                st.error(f"Invalid key: {exc}")
                st.session_state.api_key_valid = False
        else:
            st.info("Paste your Gemini API key to begin.", icon="ℹ️")
            st.session_state.api_key_valid = False

        st.divider()

        # ── Topic picker ──────────────────────────────────────────────────────
        st.markdown("### 📚 Interview Topic")
        topic_names = list(TOPICS.keys())
        selected_topic = st.selectbox(
            "Choose topic",
            topic_names,
            label_visibility="collapsed",
        )
        meta = TOPICS[selected_topic]
        st.markdown(
            f"<div class='topic-badge'>{meta['icon']} {selected_topic}</div>"
            f"<p class='topic-desc'>{meta['description']}</p>",
            unsafe_allow_html=True,
        )
        # Show tag pills
        tags_html = " ".join(
            f"<span class='tag'>{t}</span>" for t in meta["tags"]
        )
        st.markdown(f"<div class='tag-row'>{tags_html}</div>", unsafe_allow_html=True)

        st.divider()

        # ── Difficulty picker ─────────────────────────────────────────────────
        st.markdown("### 🎚️ Difficulty")
        selected_difficulty = st.radio(
            "Difficulty",
            DIFFICULTIES,
            label_visibility="collapsed",
            horizontal=False,
        )
        diff_meta = DIFFICULTY_META[selected_difficulty]
        st.markdown(
            f"<span style='color:{diff_meta['color']}; font-weight:600;'>"
            f"{diff_meta['icon']} {selected_difficulty}</span> "
            f"<span style='font-size:12px; color:#888;'>— {diff_meta['desc']}</span>",
            unsafe_allow_html=True,
        )

        st.divider()

        # ── Stats ─────────────────────────────────────────────────────────────
        history = st.session_state.history
        if history:
            avg_score = sum(h["score"] for h in history) / len(history)
            c1, c2 = st.columns(2)
            c1.metric("Sessions", len(history))
            c2.metric("Avg Score", f"{avg_score:.1f}/10")

        # Store selections so main content can read them
        st.session_state.selected_topic = selected_topic
        st.session_state.selected_difficulty = selected_difficulty


# ─────────────────────────────────────────────────────────────────────────────
# Main content
# ─────────────────────────────────────────────────────────────────────────────

def render_main_content() -> None:
    """Render the central panel: question → answer → feedback → history."""

    if not st.session_state.get("api_key_valid"):
        _render_landing()
        return

    topic      = st.session_state.selected_topic
    difficulty = st.session_state.selected_difficulty

    # ── Generate question ─────────────────────────────────────────────────────
    col_gen, col_clear = st.columns([1, 1])
    with col_gen:
        if st.button(
            "⚡ Generate Question",
            type="primary",
            use_container_width=True,
            disabled=st.session_state.generating,
        ):
            _do_generate(topic, difficulty)

    with col_clear:
        if st.button("🔄 Start Over", use_container_width=True):
            _reset_question()

    # ── Display current question ──────────────────────────────────────────────
    if st.session_state.generating:
        with st.spinner("Generating question…"):
            pass

    if st.session_state.current_question:
        diff_color = DIFFICULTY_META[st.session_state.question_difficulty]["color"]
        icon       = TOPICS[st.session_state.question_topic]["icon"]

        st.markdown(
            f"""
            <div class="question-card">
                <div class="question-meta">
                    {icon} <strong>{st.session_state.question_topic}</strong>
                    &nbsp;·&nbsp;
                    <span style="color:{diff_color};">
                        {DIFFICULTY_META[st.session_state.question_difficulty]['icon']}
                        {st.session_state.question_difficulty}
                    </span>
                </div>
                <p class="question-text">{st.session_state.current_question}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("### ✍️ Your Answer")
        st.session_state.user_answer = st.text_area(
            "Type your answer here…",
            value=st.session_state.user_answer,
            height=200,
            placeholder="Explain your thought process clearly. Include examples where possible.",
            label_visibility="collapsed",
        )

        # Word count hint
        word_count = len(st.session_state.user_answer.split()) if st.session_state.user_answer.strip() else 0
        color = "#1D9E75" if word_count >= 50 else "#BA7517" if word_count >= 20 else "#888"
        st.markdown(
            f"<p style='font-size:12px; color:{color}; margin-top:-8px;'>"
            f"📝 {word_count} words "
            f"{'✓ Good length' if word_count >= 50 else '(aim for 50+ words for best feedback)'}"
            f"</p>",
            unsafe_allow_html=True,
        )

        # ── Evaluate button ───────────────────────────────────────────────────
        if st.button(
            "🧠 Evaluate My Answer",
            type="primary",
            use_container_width=True,
            disabled=st.session_state.evaluating or not st.session_state.user_answer.strip(),
        ):
            _do_evaluate()

        if st.session_state.evaluating:
            with st.spinner("AI is analysing your answer…"):
                pass

        # ── Feedback panel ────────────────────────────────────────────────────
        if st.session_state.evaluation_done and st.session_state.feedback:
            _render_feedback(st.session_state.feedback)

    # ── History ───────────────────────────────────────────────────────────────
    if st.session_state.history:
        _render_history()


# ─────────────────────────────────────────────────────────────────────────────
# Feedback renderer
# ─────────────────────────────────────────────────────────────────────────────

def _render_feedback(fb: dict) -> None:
    """Render the structured AI feedback below the answer box."""
    score   = fb.get("score", 0)
    verdict = fb.get("verdict", "N/A")
    color   = SCORE_COLOURS.get(verdict, "#888")

    st.markdown("---")
    st.markdown("## 📊 AI Feedback")

    # ── Score card row ────────────────────────────────────────────────────────
    c1, c2, c3 = st.columns([1, 1, 2])
    with c1:
        st.markdown(
            f"""
            <div class="score-card" style="border-color:{color};">
                <div class="score-number" style="color:{color};">{score}<span>/10</span></div>
                <div class="score-label">Score</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            f"""
            <div class="score-card" style="border-color:{color};">
                <div class="score-verdict" style="color:{color};">{verdict}</div>
                <div class="score-label">Verdict</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c3:
        # Progress bar
        pct = int(score * 10)
        st.markdown(f"**Performance: {pct}%**")
        st.progress(pct / 100)
        st.caption(f"You scored {score} out of 10 on this question.")

    st.markdown("")

    # ── Strengths & improvements ──────────────────────────────────────────────
    col_s, col_i = st.columns(2)

    with col_s:
        st.markdown(
            "<div class='feedback-box strengths-box'>"
            "<h4>✅ Strengths</h4>",
            unsafe_allow_html=True,
        )
        strengths = fb.get("strengths") or []
        if strengths:
            for point in strengths:
                st.markdown(f"- {point}")
        else:
            st.markdown("_No specific strengths noted._")
        st.markdown("</div>", unsafe_allow_html=True)

    with col_i:
        st.markdown(
            "<div class='feedback-box improvements-box'>"
            "<h4>🔧 Areas to Improve</h4>",
            unsafe_allow_html=True,
        )
        improvements = fb.get("improvements") or []
        if improvements:
            for point in improvements:
                st.markdown(f"- {point}")
        else:
            st.markdown("_No improvements needed._")
        st.markdown("</div>", unsafe_allow_html=True)

    # ── Ideal answer ──────────────────────────────────────────────────────────
    with st.expander("💡 View Ideal Answer", expanded=score < 7):
        st.markdown(
            f"<div class='ideal-answer'>{fb.get('ideal_answer', 'N/A')}</div>",
            unsafe_allow_html=True,
        )

    # ── Study tip ─────────────────────────────────────────────────────────────
    tip = fb.get("tips", "")
    if tip:
        st.info(f"📚 **Study Tip:** {tip}", icon="💡")


# ─────────────────────────────────────────────────────────────────────────────
# History renderer
# ─────────────────────────────────────────────────────────────────────────────

def _render_history() -> None:
    """Render collapsible history of past Q&A sessions."""
    st.markdown("---")
    st.markdown("## 📜 Session History")

    for i, record in enumerate(reversed(st.session_state.history), 1):
        verdict = record.get("verdict", "N/A")
        color   = SCORE_COLOURS.get(verdict, "#888")
        label   = (
            f"#{len(st.session_state.history) - i + 1} · "
            f"{record['topic']} ({record['difficulty']}) · "
            f"Score: {record['score']}/10 — {verdict}"
        )
        with st.expander(label):
            st.markdown(f"**Question:** {record['question']}")
            st.markdown(f"**Your Answer:** {record['answer'][:300]}{'…' if len(record['answer']) > 300 else ''}")
            st.markdown(
                f"<span style='color:{color}; font-weight:600;'>Score: {record['score']}/10 — {verdict}</span>",
                unsafe_allow_html=True,
            )

    if st.button("🗑️ Clear History"):
        st.session_state.history = []
        st.rerun()


# ─────────────────────────────────────────────────────────────────────────────
# Landing screen (shown when no API key is set)
# ─────────────────────────────────────────────────────────────────────────────

def _render_landing() -> None:
    """Show onboarding cards when the API key is not yet configured."""
    st.markdown("### 👋 Welcome! Get started in 3 steps:")
    c1, c2, c3 = st.columns(3)
    for col, icon, title, desc in [
        (c1, "🔑", "1. Add API Key", "Paste your free Google Gemini API key in the sidebar."),
        (c2, "📚", "2. Pick a Topic", "Choose from Python, SQL, OOP, ML, and more."),
        (c3, "🎯", "3. Practice!",   "Generate questions, answer them, get instant AI feedback."),
    ]:
        with col:
            st.markdown(
                f"<div class='landing-card'>"
                f"<div class='landing-icon'>{icon}</div>"
                f"<h4>{title}</h4>"
                f"<p>{desc}</p>"
                f"</div>",
                unsafe_allow_html=True,
            )

    st.markdown("---")
    st.markdown(
        "🔗 Get your free Gemini API key at "
        "[Google AI Studio](https://aistudio.google.com/app/apikey)"
    )


# ─────────────────────────────────────────────────────────────────────────────
# Action helpers
# ─────────────────────────────────────────────────────────────────────────────

def _do_generate(topic: str, difficulty: str) -> None:
    """Trigger question generation and update session state."""
    st.session_state.generating      = True
    st.session_state.evaluation_done = False
    st.session_state.feedback        = None
    st.session_state.user_answer     = ""
    try:
        question = generate_question(topic, difficulty)
        st.session_state.current_question    = question
        st.session_state.question_topic      = topic
        st.session_state.question_difficulty = difficulty
    except RuntimeError as exc:
        st.error(f"❌ {exc}")
    finally:
        st.session_state.generating = False


def _do_evaluate() -> None:
    """Trigger evaluation and update session state."""
    st.session_state.evaluating = True
    try:
        feedback = evaluate_answer(
            topic      = st.session_state.question_topic,
            difficulty = st.session_state.question_difficulty,
            question   = st.session_state.current_question,
            answer     = st.session_state.user_answer,
        )
        st.session_state.feedback        = feedback
        st.session_state.evaluation_done = True

        # Save to history
        st.session_state.history.append({
            "topic":      st.session_state.question_topic,
            "difficulty": st.session_state.question_difficulty,
            "question":   st.session_state.current_question,
            "answer":     st.session_state.user_answer,
            "score":      feedback["score"],
            "verdict":    feedback["verdict"],
        })
    except (RuntimeError, ValueError) as exc:
        st.error(f"❌ {exc}")
    finally:
        st.session_state.evaluating = False


def _reset_question() -> None:
    """Clear the current question, answer, and feedback."""
    st.session_state.current_question = None
    st.session_state.user_answer      = ""
    st.session_state.feedback         = None
    st.session_state.evaluation_done  = False
