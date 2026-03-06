import requests
import os

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

def ask_ai(question):
    url = "https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash-latest:generateContent"

    headers = {
        "Content-Type": "application/json"
    }

    data = {
        "contents": [
            {
                "parts": [
                    {"text": question}
                ]
            }
        ]
    }

    response = requests.post(
        url + "?key=" + GEMINI_API_KEY,
        headers=headers,
        json=data
    )

    result = response.json()

    print("Full API response:", result)

    try:
        return result["candidates"][0]["content"]["parts"][0]["text"]
    except:
        return "AI did not return a response"
