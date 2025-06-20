import gradio as gr
from src.extractor import extract_text_from_pdf
from src.analyzer import (
    score_resume_against_jd,
    find_missing_skills,
    generate_feedback,
    gpt_resume_feedback
)

def analyze_resume(resume_file, jd_file):
    if not resume_file or not jd_file:
        return "Missing file(s)", "", "", ""

    resume_text = extract_text_from_pdf(resume_file.name)
    jd_text = jd_file

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
