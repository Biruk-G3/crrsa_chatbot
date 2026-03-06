import os
import requests

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

def ask_ai(question):
    if not GEMINI_API_KEY:
        return "Gemini API key is missing"

    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-3-flash-preview:generateContent?key={GEMINI_API_KEY}"

    headers = {"Content-Type": "application/json"}
    data = {"contents":[{"parts":[{"text": question}]}]}

    response = requests.post(url, headers=headers, json=data)
    result = response.json()
    print("Full API response:", result)

    try:
        return result["candidates"][0]["content"]["parts"][0]["text"]
    except:
        return "AI did not return a response"
