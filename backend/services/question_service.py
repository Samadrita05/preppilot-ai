from core.ollama_client import ask_ollama


def generate_questions(role: str, difficulty: str):
    prompt = f"""
You are a senior technical interviewer.

Generate exactly 5 interview questions for a {difficulty} level {role} position.

IMPORTANT RULES:
- Questions must be strictly related to {role}.
- Do NOT generate general DSA, array, sorting, OOP, or generic programming questions 
  unless they are directly relevant to {role}.
- Focus on real-world tools, concepts, frameworks, and practical knowledge used in {role}.
- Avoid repetition.
- Return ONLY the 5 questions as a numbered list.
- Do not add explanations or extra text.
"""

    ai_response = ask_ollama(prompt)

    questions = [
        q.strip("0123456789. ").strip()
        for q in ai_response.split("\n")
        if q.strip()
    ]

    return questions
