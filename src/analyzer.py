import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from keybert import KeyBERT

# Initialize KeyBERT model
kw_model = KeyBERT(model='all-MiniLM-L6-v2')

# ✅ Score similarity between resume and JD using TF-IDF
def score_resume_against_jd(resume_text, jd_text):
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform([resume_text, jd_text])
    score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    return round(score * 100, 2)

# ✅ Extract top keywords using KeyBERT
def extract_keywords(text, top_n=20):
    keywords = kw_model.extract_keywords(text, top_n=top_n, stop_words='english')
    return [kw[0] for kw in keywords if len(kw[0]) > 2]

# ✅ Find which job description keywords are missing in the resume
def find_missing_skills(resume_text, jd_text, top_n=20):
    jd_keywords = extract_keywords(jd_text, top_n)
    resume_words = set(resume_text.lower().split())
    missing = [kw for kw in jd_keywords if kw.lower() not in resume_words]
    return missing

# ✅ Rule-based suggestions
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

