import os
import requests

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

def ask_ai(question):
    if not GEMINI_API_KEY:
        return "Gemini API key is missing"

    # Use a working model
    model_name = "models/gemini-2.5-flash"
    url = f"https://generativelanguage.googleapis.com/v1/{model_name}:generateContent?key={GEMINI_API_KEY}"

    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [
            {"parts": [{"text": question}]}
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        result = response.json()
        print("Full API response:", result)

        return result["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        print("Error generating content:", e)
        return "AI did not return a response"
