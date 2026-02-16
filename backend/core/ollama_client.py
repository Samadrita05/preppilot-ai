import requests
import os

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

MODEL_NAME = "llama-3.1-8b-instant"

def ask_ollama(prompt: str) -> str:
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post(
        GROQ_URL,
        headers=headers,
        json=data,
        timeout=60
    )

    if response.status_code != 200:
        print(response.text)  # This will show real Groq error
        response.raise_for_status()

    result = response.json()

    return result["choices"][0]["message"]["content"]
