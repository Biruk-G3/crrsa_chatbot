import requests
import os

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

def ask_ai(question):

    if not GEMINI_API_KEY:
        return "Gemini API key is missing"

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

    print("Status code:", response.status_code)

    result = response.json()

    print("Full API response:", result)

    if response.status_code != 200:
        return "AI request failed"

    try:
        return result["candidates"][0]["content"]["parts"][0]["text"]
    except:
        return "AI did not return a response"
