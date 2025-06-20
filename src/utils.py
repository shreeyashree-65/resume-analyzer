import json

def save_feedback_txt(score, missing_keywords, feedback, gpt_feedback, output_path):
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(f"Resume Score: {score:.2f}%\n\n")
        f.write("Missing Keywords:\n")
        for kw in missing_keywords:
            f.write(f"- {kw}\n")
        f.write("\nRule-Based Feedback:\n")
        for tip in feedback:
            f.write(f"- {tip}\n")
        f.write("\nGPT-Powered Feedback:\n")
        f.write(gpt_feedback + "\n")

def save_feedback_json(score, missing_keywords, feedback, gpt_feedback, output_path):
    result = {
        "score": score,
        "missing_keywords": missing_keywords,
        "rule_based_feedback": feedback,
        "gpt_feedback": gpt_feedback
    }
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2)

def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()
