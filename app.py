import gradio as gr
from src.extractor import extract_text_from_pdf
from src.analyzer import (
    score_resume_against_jd,
    find_missing_skills,
    generate_feedback,
    gpt_resume_feedback
)

def analyze_resume(resume_file, jd_file):
    import os
    from src.utils import read_file
    from src.extractor import extract_text_from_pdf

    # Check file presence
    if resume_file is None or jd_file is None:
        return "Missing file(s)", "", "", ""

    # Extract resume text using pdfplumber
    try:
        resume_path = resume_file.name if hasattr(resume_file, "name") else resume_file
        resume_text = extract_text_from_pdf(resume_path)
    except Exception as e:
        return "", "", "", f"❌ Failed to read resume: {e}"

    # Extract JD text using plain read
    try:
        jd_path = jd_file.name if hasattr(jd_file, "name") else jd_file
        jd_text = read_file(jd_path)
    except Exception as e:
        return "", "", "", f"❌ Failed to read job description: {e}"

    # Check if text is too short
    if len(resume_text.strip()) < 100 or len(jd_text.strip()) < 50:
        return "", "", "⚠️ Could not extract enough meaningful text.", ""

    # Analysis
    score = score_resume_against_jd(resume_text, jd_text)
    missing = find_missing_skills(resume_text, jd_text)
    rule_feedback = generate_feedback(score, missing)
    gpt_feedback = gpt_resume_feedback(resume_text, jd_text, missing)

    return (
        f"{score:.2f}%",
        "\n".join(missing) if missing else "✅ No missing keywords!",
        "\n".join(rule_feedback),
        gpt_feedback
    )

with gr.Blocks() as demo:
    gr.Markdown("# 🤖 Resume Analyzer (with GPT)")
    
    with gr.Row():
        resume_input = gr.File(label="Upload Resume (PDF)", file_types=[".pdf"])
        jd_input = gr.File(label="Upload Job Description (TXT)", file_types=[".txt"])
    
    analyze_btn = gr.Button("Analyze Resume")

    score_output = gr.Textbox(label="Score")
    missing_output = gr.Textbox(label="Missing Keywords")
    rule_feedback_output = gr.Textbox(label="Rule-Based Feedback")
    gpt_feedback_output = gr.Textbox(label="GPT Feedback")

    analyze_btn.click(
        analyze_resume,
        inputs=[resume_input, jd_input],
        outputs=[score_output, missing_output, rule_feedback_output, gpt_feedback_output]
    )

demo.launch()
