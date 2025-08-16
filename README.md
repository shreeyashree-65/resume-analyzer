# 🤖 Resume Analyzer

A simple basic web app to compare your resume against a job description and receive instant feedback.

---

## 🚀 Features
-  **PDF Parsing** – Extract structured text from resumes using `pdfplumber`.
-  **Keyword Extraction** – Identify important skills and terms with `KeyBERT` and `sentence-transformers`.
-  **NLP Processing** – Use `spaCy` and `Hugging Face Transformers` for named entity recognition (NER), embeddings, and contextual analysis.
-  **Skill/Score Evaluation** – Leverage `scikit-learn` models for classification and scoring.
-  **Interactive Demo** – `Gradio` interface for uploading resumes and viewing results instantly.

---

## 📁 Project Structure

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
## 🛠️ Tech Stack

**Languages**  
- Python  

**Libraries & Frameworks**  
- [pdfplumber] – PDF text extraction  
- [spaCy] – NLP processing  
- [Hugging Face Transformers] – contextual embeddings  
- [sentence-transformers] – semantic similarity  
- [KeyBERT] – keyword extraction  
- [scikit-learn] – ML utilities and scoring  
- [Gradio] – user-friendly frontend  

**Tools**  
- Git, GitHub, VSCode, Postman (for API testing)

---
## How It Works
1. Upload a resume (PDF) through the Gradio interface.  
2. The system parses the text and cleans it.  
3. NLP models analyze content for keywords, entities, and embeddings.  
4. Candidate resume is scored against required skills or job description.  
5. Results are displayed with extracted keywords, skills, and recommendations.  

---
## How to Run

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

### Sample Files

Use `sample_resume.pdf` and `sample-jobd.txt` from the `data/` folder for testing.

---
