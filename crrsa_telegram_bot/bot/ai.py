import google.generativeai as genai
import os

genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")

def ask_ai(question):
    try:
        response = model.generate_content(question)
        return response.text
    except Exception as e:
        return f"AI Error: {str(e)}"
