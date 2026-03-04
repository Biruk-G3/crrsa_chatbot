import os
import openai  # if using OpenAI

# set API key in Render environment variables
openai.api_key = os.environ.get("OPENAI_API_KEY")

def ask_ai(question):
    if not question:
        return "Please ask a question."

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role":"user","content": question}],
            max_tokens=200
        )
        answer = response['choices'][0]['message']['content']
        return answer
    except Exception as e:
        return f"Error: {str(e)}"
