# main.py
from src.utils import save_feedback_txt, save_feedback_json
from src.extractor import extract_text_from_pdf, extract_sections
from src.analyzer import (
    score_resume_against_jd,
    extract_keywords,
    find_missing_skills,
    generate_feedback,
    gpt_resume_feedback
)
from src.utils import read_file

resume_path = 'data/sample_resume.pdf'
jd_path = 'data/job_description.txt'

resume_text = extract_text_from_pdf(resume_path)
jd_text = read_file(jd_path)

sections = extract_sections(resume_text)
score = score_resume_against_jd(resume_text, jd_text)
keywords = extract_keywords(jd_text)

print("🔍 Resume Analysis")
print("------------------")
print(f"Score Against Job Description: {score}%\n")

print("📘 Sections Extracted:")
for key, values in sections.items():
    print(f"\n{key.upper()}:")
    for val in values:
        print(f"- {val}")

print("\n📌 Top Keywords in JD:")
for kw in keywords:
    print(f"- {kw}")

missing_skills = find_missing_skills(resume_text, jd_text)

print("\n🚨 Missing Keywords from Resume (based on JD):")
if missing_skills:
    for skill in missing_skills:
        print(f"- {skill}")
else:
    print("✅ All key skills covered!")

# Generate Feedback
feedback = generate_feedback(score, missing_skills)

print("\n💬 Resume Feedback:")
print("--------------------")
for tip in feedback:
    print(tip)

# GPT Feedback
print("\n GPT-Powered Feedback:")
gpt_response = gpt_resume_feedback(resume_text, jd_text, missing_skills)
print(gpt_response)

# Save output
save_feedback_txt(score, missing_skills, feedback, gpt_response, "output/analysis.txt")
save_feedback_json(score, missing_skills, feedback, gpt_response, "output/analysis.json")

print("\n✅ Feedback saved to 'output/analysis.txt' and 'output/analysis.json'")
