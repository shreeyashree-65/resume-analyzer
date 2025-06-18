import pdfplumber
import re

def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

def extract_sections(text):
    sections = {
        "education": [],
        "experience": [],
        "skills": []
    }

    lines = text.split('\n')
    for line in lines:
        lower = line.lower()
        if "bachelor" in lower or "university" in lower or "education" in lower:
            sections["education"].append(line)
        elif "experience" in lower or "intern" in lower or "worked" in lower:
            sections["experience"].append(line)
        elif "skills" in lower or re.search(r'\bpython\b|\bjava\b|\bc++\b|\bml\b', lower):
            sections["skills"].append(line)

    return sections
