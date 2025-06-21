# 🤖 Resume Analyzer

A simple basic web app to compare your resume against a job description and receive instant feedback.

---

### 🚀 Features

- 📄 Extracts text from PDF resumes
- 📑 Analyzes job descriptions (TXT files)
- 📊 Gives a match score
- 🔍 Identifies missing keywords
- 💡 Provides rule-based feedback to improve your resume

---

### 📁 Project Structure

```
resume-analyzer/
├── app.py                  # Main Gradio app
├── src/
│   ├── analyzer.py         # Scoring and feedback logic
│   ├── extractor.py        # PDF text extraction
│   └── utils.py            # File reading helpers
├── data/                   # Sample data for testing
│   ├── sample_resume.pdf
│   └── sample-jobd.txt
├── .env                    # (ignored) API keys or config (not used)
├── .gitignore
└── requirements.txt        # Python dependencies
```

---

### ✅ How to Run

1. **Install dependencies**

```bash
pip install -r requirements.txt
```

2. **Start the app**

```bash
python app.py
```

3. **Open in browser**

Visit: `http://127.0.0.1:7860`

---

### 📦 Sample Files

Use `sample_resume.pdf` and `sample-jobd.txt` from the `data/` folder for testing.

---
