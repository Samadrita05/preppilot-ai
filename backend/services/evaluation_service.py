from core.ollama_client import ask_ollama
import re

# 🔹 Per-question evaluation
def evaluate_answer(user_answer: str, question_text: str):
    prompt = f"""
You are a technical interviewer.

Question:
{question_text}

Candidate Answer:
{user_answer}

Evaluate the answer and return STRICTLY in this format:

Score: <number out of 10>
Feedback: <short constructive feedback>
"""

    response = ask_ollama(prompt)

    score = None
    feedback = None

    for line in response.splitlines():
        line_lower = line.lower().strip()

        # ✅ Robust score extraction
        if line_lower.startswith("score"):
            match = re.search(r"(\d+(\.\d+)?)", line)
            if match:
                score = float(match.group(1))

        # ✅ Robust feedback extraction
        if line_lower.startswith("feedback"):
            feedback = line.split(":", 1)[1].strip()

    # Fallback safety
    if feedback is None:
        feedback = response.strip()

    return score, feedback


# 🔹 Overall interview evaluation (UNCHANGED)
def evaluate_overall(answers: list[str]):
    combined_answers = "\n".join(answers)

    prompt = f"""
You are an interview evaluator.

Based on the following answers, give:
- Overall performance (out of 10)
- Strengths
- Weaknesses
- Final verdict (Hire / Maybe / Reject)

Answers:
{combined_answers}
"""

    return ask_ollama(prompt)
