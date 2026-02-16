from core.ollama_client import ask_ollama

def evaluate_answer(user_answer: str, ideal_answer: str | None):
    if not ideal_answer:
        return 7.0, "Good attempt. No ideal answer available."

    prompt = f"""
You are an interview evaluator.

Ideal Answer:
{ideal_answer}

Candidate Answer:
{user_answer}

Tasks:
1. Give a score out of 10
2. Give short constructive feedback

Respond strictly in this format:
Score: X/10
Feedback: <one paragraph>
"""

    ai_response = ask_ollama(prompt)

    # Basic parsing
    try:
        score_line = [l for l in ai_response.splitlines() if "Score" in l][0]
        score = float(score_line.split(":")[1].split("/")[0].strip())
    except:
        score = 7.0

    feedback = ai_response.split("Feedback:", 1)[-1].strip()

    return score, feedback
