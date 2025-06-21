import gradio as gr
from src.extractor import extract_text_from_pdf
from src.analyzer import (
    score_resume_against_jd,
    find_missing_skills,
    generate_feedback,
    gpt_resume_feedback
)

def analyze_resume(resume_file, jd_file):
    from src.utils import read_file
    from src.extractor import extract_text_from_pdf
    import traceback

    try:
        # Validate file presence
        if resume_file is None or jd_file is None:
            return (
                "❌ Missing file(s)",
                [{"text": "No file uploaded", "entity": "ERROR"}],
                "Please upload both resume and job description.",
                "Upload files to get GPT feedback."
            )

        # Extract resume text
        resume_path = resume_file.name if hasattr(resume_file, "name") else resume_file
        resume_text = extract_text_from_pdf(resume_path)

        # Extract JD text
        jd_path = jd_file.name if hasattr(jd_file, "name") else jd_file
        jd_text = read_file(jd_path)

        if len(resume_text.strip()) < 100 or len(jd_text.strip()) < 50:
            return (
                "❌ Not enough content",
                [{"text": "File too short", "entity": "ERROR"}],
                "Ensure both resume and JD have enough content.",
                "Too little content to analyze."
            )

        # Perform analysis
        score = score_resume_against_jd(resume_text, jd_text)
        missing = find_missing_skills(resume_text, jd_text)
        rule_feedback = generate_feedback(score, missing)
        gpt_feedback = gpt_resume_feedback(resume_text, jd_text, missing)

        # Highlight missing
        highlighted = [{"text": kw, "start": 0, "end": len(kw), "entity": "MISSING"} for kw in missing] if missing else [{"text": "✅ No missing keywords!", "entity": "NONE"}]

        return (
            f"{score:.2f}%",
            highlighted,
            "\n".join(rule_feedback),
            gpt_feedback
        )

    except Exception as e:
        traceback.print_exc()  # Prints to terminal / Gradio logs
        return (
            "❌ Internal error",
            [{"text": str(e), "entity": "ERROR"}],
            "An error occurred during processing.",
            f"❌ GPT Feedback failed: {e}"
        )

with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🤖 Resume Analyzer (with GPT)")
    
    with gr.Row():
        resume_input = gr.File(label="Upload Resume (PDF)", file_types=[".pdf"])
        jd_input = gr.File(label="Upload Job Description (TXT)", file_types=[".txt"])
    
    analyze_btn = gr.Button("Analyze Resume")

    score_output = gr.Textbox(label="Score")
    missing_output = gr.HighlightedText(
    label="Missing Keywords",
    combine_adjacent=True)
    rule_feedback_output = gr.Textbox(label="Rule-Based Feedback")
    gpt_feedback_output = gr.Textbox(label="GPT Feedback")

    analyze_btn.click(
        analyze_resume,
        inputs=[resume_input, jd_input],
        outputs=[score_output, missing_output, rule_feedback_output, gpt_feedback_output]
    )

demo.launch()
