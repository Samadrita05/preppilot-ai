import ollama

response = ollama.chat(
    model='llama3.1:8b',
    messages=[
        {'role': 'user', 'content': 'Generate 3 interview questions for a Python developer'}
    ]
)

print(response['message']['content'])
