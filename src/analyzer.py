import openai
import os
import re
from keybert import KeyBERT
from dotenv import load_dotenv
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Score using cosine similarity
def score_resume_against_jd(resume_text, jd_text):
    tfidf = TfidfVectorizer(stop_words="english")
    tfidf_matrix = tfidf.fit_transform([resume_text, jd_text])
    score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    return round(score * 100, 2)

# Clean & extract keywords using TF-IDF
def extract_keywords(text, top_n=20):
    kw_model = KeyBERT(model='all-MiniLM-L6-v2')  # Lightweight & fast
    keywords = kw_model.extract_keywords(text, top_n=top_n, stop_words='english')
    return [kw[0] for kw in keywords]

# Find JD keywords not present in resume
def find_missing_skills(resume_text, jd_text, top_n=20):
    jd_keywords = extract_keywords(jd_text, top_n)
    resume_keywords = extract_keywords(resume_text, top_n=50)
    missing = [kw for kw in jd_keywords if kw not in resume_keywords]
    return missing

# Give score-based & keyword feedback
def generate_feedback(score, missing_keywords):
    feedback = []

    if score < 40:
        feedback.append("Your resume is a poor match for the job. Consider tailoring it more carefully.")
    elif score < 70:
        feedback.append("Your resume is a partial match. Improve it by adding relevant skills and aligning experiences.")
    else:
        feedback.append("Your resume is a good match. Fine-tune the language and examples to maximize impact.")

    if missing_keywords:
        feedback.append("Consider including these skills or tools in your resume (if you have experience):")
        feedback.extend([f"- {kw}" for kw in missing_keywords])
    else:
        feedback.append("✅ You’ve covered all key job-related keywords. Good job!")

    return feedback

# GPT-based personalized suggestions
def gpt_resume_feedback(resume_text, jd_text, missing_keywords):
    openai.api_key = os.getenv("OPENAI_API_KEY")

    prompt = f"""
You are a resume coach. Analyze the following resume in the context of the job description.

Job Description:
{jd_text}

Resume:
{resume_text}

Missing keywords:
{', '.join(missing_keywords)}

Provide 3 personalized suggestions to improve the resume. Be constructive and actionable.
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=300
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"❌ GPT Feedback failed: {e}"

# Load env vars
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
