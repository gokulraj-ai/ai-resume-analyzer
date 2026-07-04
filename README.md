# 🎯 AI Interview Preparation Assistant

> Generate real technical interview questions, answer them, and get instant AI-powered feedback — powered by Google Gemini.

---

## ✨ Features

| Feature | Details |
|---|---|
| **8 Topics** | Python, SQL, OOP, Data Structures, ML, System Design, JavaScript, Django/Flask |
| **3 Difficulty Levels** | Easy · Medium · Hard |
| **AI Question Generation** | Unique, topic-specific questions every time |
| **AI Answer Evaluation** | Score out of 10, verdict, strengths, improvements, ideal answer |
| **Study Tips** | Personalised tip after every evaluation |
| **Session History** | All your past Q&As in one collapsible panel |
| **Clean UI** | Streamlit + custom CSS, dark-mode friendly |

---

## 🗂️ Project Structure

```
ai_interview_prep/
├── app.py                  # Entry point — run this with streamlit
├── requirements.txt        # Python dependencies
├── .env.example            # Template for optional env-based key storage
├── .gitignore
├── README.md
├── assets/
│   └── style.css           # Custom CSS for the UI
└── src/
    ├── __init__.py
    ├── config.py           # Topics, difficulties, score colours
    ├── gemini.py           # Gemini API client (question gen + evaluation)
    ├── session.py          # Streamlit session_state initialiser
    └── ui.py               # All rendering functions (header, sidebar, main)
```

---

## 🚀 Installation & Setup

### 1. Clone or download the project

```bash
git clone https://github.com/<your-username>/ai-interview-prep.git
cd ai-interview-prep
```

### 2. Create and activate a virtual environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Get your free Gemini API key

1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Click **"Create API key"** → copy the key

### 5. Run the app

```bash
streamlit run app.py
```

The app opens at **http://localhost:8501** in your browser.

---

## 🔑 API Key Options

**Option A — Enter via the UI (easiest)**
Paste the key in the sidebar text box. It is never stored on disk.

**Option B — Streamlit secrets (recommended for deployment)**
```toml
# .streamlit/secrets.toml
GEMINI_API_KEY = "AIza..."
```

**Option C — `.env` file**
```bash
cp .env.example .env
# Edit .env and add your key
```

---

## 🖥️ Usage

1. Open the app and paste your Gemini API key in the sidebar.
2. Select an **Interview Topic** and **Difficulty**.
3. Click **⚡ Generate Question**.
4. Type your answer in the text area (aim for 50+ words).
5. Click **🧠 Evaluate My Answer**.
6. Read your score, verdict, strengths, improvements, and the ideal answer.
7. Repeat — your history is saved for the session.

---

## 📤 Upload to GitHub

```bash
# Inside the project folder:
git init
git add .
git commit -m "Initial commit: AI Interview Prep Assistant"

# Create a new repo on github.com, then:
git remote add origin https://github.com/<your-username>/ai-interview-prep.git
git branch -M main
git push -u origin main
```

---

## 🛠️ Extending the App

**Add a new topic** — edit `src/config.py`, add an entry to `TOPICS`. Done.

**Change the model** — edit `GEMINI_MODEL` in `src/gemini.py`.

**Adjust scoring prompts** — edit `EVALUATION_PROMPT` in `src/gemini.py`.

---

## 📦 Dependencies

| Package | Purpose |
|---|---|
| `streamlit` | Web UI framework |
| `google-generativeai` | Official Gemini Python SDK |

---

## 👤 Author

**Gokul Raj D** — B.E. Electronics & Communication Engineering  
MNM Jain Engineering College · GitHub: [gokulrajd1913-pixel](https://github.com/gokulrajd1913-pixel)

---

## 📄 License

MIT — free to use, modify, and distribute.
