from core.ollama_client import ask_ollama

def generate_feedback(question: str, user_answer: str):
    prompt = f"""
You are an interview coach.

Question:
{question}

Candidate Answer:
{user_answer}

Give clear feedback with:
- What is correct
- What is missing
- How to improve
"""

    return ask_ollama(prompt)
