from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def score_resume_against_jd(resume_text, jd_text):
    tfidf = TfidfVectorizer()
    tfidf_matrix = tfidf.fit_transform([resume_text, jd_text])
    score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    return round(score * 100, 2)

def extract_keywords(text, top_n=10):
    tfidf = TfidfVectorizer(stop_words='english', max_features=top_n)
    tfidf_matrix = tfidf.fit_transform([text])
    return tfidf.get_feature_names_out()

def find_missing_skills(resume_text, jd_text, top_n=20):
    # Extract top job description keywords
    jd_keywords = extract_keywords(jd_text, top_n=top_n)
    # Lowercase for matching
    resume_words = set(resume_text.lower().split())
    # Find which JD keywords are missing in resume
    missing = [kw for kw in jd_keywords if kw.lower() not in resume_words]
    return missing

def generate_feedback(score, missing_keywords):
    feedback = []
    # Score-based feedback
    if score < 40:
        feedback.append("Your resume is a poor match for the job. Consider tailoring it more carefully.")
    elif score < 70:
        feedback.append("Your resume is a partial match. Improve it by adding relevant skills and aligning experiences.")
    else:
        feedback.append("Your resume is a good match. Fine-tune the language and examples to maximize impact.")
    # Missing skill feedback
    if missing_keywords:
        feedback.append("Consider including these skills or tools in your resume (if you have experience):")
        feedback.extend([f"- {kw}" for kw in missing_keywords])
    else:
        feedback.append("✅ You’ve covered all key job-related keywords. Good job!")
    return feedback
