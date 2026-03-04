import os
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def ask_ai(question):
    if not question:
        return "Please ask a question."
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": question}],
            max_tokens=200
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"
