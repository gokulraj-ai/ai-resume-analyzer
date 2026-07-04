"""
gemini.py — Thin wrapper around the Google Gemini API.

Responsibilities:
  • Configure the SDK with the user's API key.
  • Generate interview questions for a given topic + difficulty.
  • Evaluate a user's answer and return structured JSON feedback.
  • Raise descriptive exceptions so the UI can show friendly error messages.
"""

import json
import re
import google.generativeai as genai


# ── Model identifier ─────────────────────────────────────────────────────────
GEMINI_MODEL = "gemini-1.5-flash"


# ── Prompt templates ─────────────────────────────────────────────────────────

QUESTION_PROMPT = """
You are a senior technical interviewer at a top-tier software company.

Generate ONE interview question on the topic: **{topic}**
Difficulty level: **{difficulty}**

Guidelines:
- The question must be clear, specific, and suitable for the stated difficulty.
- For EASY: focus on definitions and basic concepts.
- For MEDIUM: include scenario-based or design questions.
- For HARD: demand deep understanding, trade-offs, or system-design thinking.
- Return ONLY the question text — no numbering, no preamble, no follow-ups.
""".strip()

EVALUATION_PROMPT = """
You are a strict but fair technical interviewer evaluating a candidate's answer.

Topic: {topic}
Difficulty: {difficulty}

Question:
{question}

Candidate's Answer:
{answer}

Evaluate the answer and respond with ONLY a valid JSON object (no markdown fences, no extra text):

{{
  "score": <integer 0-10>,
  "verdict": "<one of: Excellent | Good | Average | Needs Improvement | Poor>",
  "strengths": ["<point 1>", "<point 2>"],
  "improvements": ["<point 1>", "<point 2>"],
  "ideal_answer": "<a concise ideal answer in 3-6 sentences>",
  "tips": "<one actionable study tip for this topic>"
}}

Scoring guide:
  9-10 → Excellent: complete, accurate, well-explained with examples
  7-8  → Good: mostly correct, minor gaps
  5-6  → Average: partially correct, important concepts missing
  3-4  → Needs Improvement: significant gaps, some correct elements
  0-2  → Poor: mostly incorrect or too brief
""".strip()


# ── Public helpers ────────────────────────────────────────────────────────────

def configure_api(api_key: str) -> None:
    """Configure the Gemini SDK. Raises ValueError for blank keys."""
    if not api_key or not api_key.strip():
        raise ValueError("API key cannot be empty.")
    genai.configure(api_key=api_key.strip())


def generate_question(topic: str, difficulty: str) -> str:
    """
    Ask Gemini to produce one interview question.

    Returns:
        The question as a plain string.
    Raises:
        RuntimeError: on any API or parsing failure.
    """
    try:
        model = genai.GenerativeModel(GEMINI_MODEL)
        prompt = QUESTION_PROMPT.format(topic=topic, difficulty=difficulty)
        response = model.generate_content(prompt)
        question = response.text.strip()
        if not question:
            raise RuntimeError("Gemini returned an empty question.")
        return question
    except Exception as exc:
        raise RuntimeError(f"Question generation failed: {exc}") from exc


def evaluate_answer(topic: str, difficulty: str, question: str, answer: str) -> dict:
    """
    Send the Q&A pair to Gemini and parse the structured feedback.

    Returns:
        dict with keys: score, verdict, strengths, improvements,
                        ideal_answer, tips
    Raises:
        RuntimeError: on API failure or unparsable response.
    """
    if not answer or not answer.strip():
        raise ValueError("Answer cannot be empty.")

    try:
        model = genai.GenerativeModel(GEMINI_MODEL)
        prompt = EVALUATION_PROMPT.format(
            topic=topic,
            difficulty=difficulty,
            question=question,
            answer=answer.strip(),
        )
        response = model.generate_content(prompt)
        raw = response.text.strip()

        # Strip accidental markdown fences if the model adds them
        raw = re.sub(r"^```(?:json)?\s*", "", raw)
        raw = re.sub(r"\s*```$", "", raw)

        feedback = json.loads(raw)
        _validate_feedback(feedback)
        return feedback

    except json.JSONDecodeError as exc:
        raise RuntimeError(
            "Gemini returned non-JSON feedback. Please try again."
        ) from exc
    except Exception as exc:
        raise RuntimeError(f"Evaluation failed: {exc}") from exc


# ── Private helpers ───────────────────────────────────────────────────────────

def _validate_feedback(feedback: dict) -> None:
    """Ensure the feedback dict has all required keys and sane values."""
    required = {"score", "verdict", "strengths", "improvements", "ideal_answer", "tips"}
    missing = required - feedback.keys()
    if missing:
        raise RuntimeError(f"Feedback JSON missing keys: {missing}")

    score = feedback.get("score")
    if not isinstance(score, (int, float)) or not (0 <= score <= 10):
        feedback["score"] = max(0, min(10, int(score or 0)))
