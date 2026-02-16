from core.ollama_client import ask_ollama
def generate_questions(role: str, difficulty: str):
    prompt = f"""
You are an interview question generator.

Role: {role}
Difficulty: {difficulty}

Generate 5 technical interview questions.
Return only the questions as a numbered list.
"""

    ai_response = ask_ollama(prompt)

    questions = [
        q.strip("0123456789. ").strip()
        for q in ai_response.split("\n")
        if q.strip()
    ]

    return questions

