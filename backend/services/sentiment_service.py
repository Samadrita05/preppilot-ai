from core.ollama_client import ask_ollama

def analyze_sentiment(answer: str):
    prompt = f"""
Analyze the tone of the following interview answer.

Answer:
{answer}

Return one word only:
Confident / Neutral / Uncertain
"""

    sentiment = ask_ollama(prompt).strip()
    return sentiment
