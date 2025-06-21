import gradio as gr
from src.extractor import extract_text_from_pdf
from src.analyzer import (
    score_resume_against_jd,
    find_missing_skills,
    generate_feedback
)

def analyze_resume(resume_file, jd_file):
    import os
    from src.utils import read_file
    from src.extractor import extract_text_from_pdf

    print("🔍 Starting resume analysis...")

    if resume_file is None or jd_file is None:
        print("⚠️ Missing files!")
        return "Missing file(s)", [], "", ""

    try:
        resume_path = resume_file.name if hasattr(resume_file, "name") else resume_file
        print("📄 Resume path:", resume_path)
        resume_text = extract_text_from_pdf(resume_path)
        print("✅ Resume text extracted.")
    except Exception as e:
        print("❌ Error reading resume:", e)
        return "", [], "", f"❌ Failed to read resume: {e}"

    try:
        jd_path = jd_file.name if hasattr(jd_file, "name") else jd_file
        print("📄 JD path:", jd_path)
        jd_text = read_file(jd_path)
        print("✅ JD text read.")
    except Exception as e:
        print("❌ Error reading JD:", e)
        return "", [], "", f"❌ Failed to read job description: {e}"

    if len(resume_text.strip()) < 100 or len(jd_text.strip()) < 50:
        print("⚠️ Not enough content extracted.")
        return "", [], "⚠️ Could not extract enough meaningful text.", ""

    print("🧠 Running analysis...")
    score = score_resume_against_jd(resume_text, jd_text)
    missing = find_missing_skills(resume_text, jd_text)
    rule_feedback = generate_feedback(score, missing)

    print("✅ Analysis complete.")

    # Format each keyword with individual entity tag for HighlightedText
    highlighted_missing = [(kw, "MISSING") for kw in missing]

    return (
        f"{score:.2f}%",
         highlighted_missing if missing else [("✅ No missing keywords!", "NONE")],
        "\n".join(rule_feedback),
)


# Build Gradio UI
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🤖 Resume Analyzer")

    with gr.Row():
        resume_input = gr.File(label="Upload Resume (PDF)", file_types=[".pdf"])
        jd_input = gr.File(label="Upload Job Description (TXT)", file_types=[".txt"])

    analyze_btn = gr.Button("Analyze Resume")

    score_output = gr.Textbox(label="Score")
    missing_output = gr.HighlightedText(label="Missing Keywords")
    rule_feedback_output = gr.Textbox(label="Rule-Based Feedback")

    analyze_btn.click(
        analyze_resume,
        inputs=[resume_input, jd_input],
        outputs=[score_output, missing_output, rule_feedback_output]
    )

demo.launch()
