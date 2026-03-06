import os
import requests

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

def ask_ai(question):
    if not GEMINI_API_KEY:
        return "Gemini API key is missing"

    # Step 1: Get available models
    try:
        list_url = f"https://generativelanguage.googleapis.com/v1/models?key={GEMINI_API_KEY}"
        list_resp = requests.get(list_url)
        list_data = list_resp.json()
        models = list_data.get("models", [])
    except Exception as e:
        print("Error fetching models:", e)
        return "AI service is currently unavailable"

    # Step 2: Pick the first model that supports generateContent
    model_name = None
    for m in models:
        if "supportedGenerationMethods" in m and "generateContent" in m["supportedGenerationMethods"]:
            model_name = m["name"]
            break

    if not model_name:
        print("No compatible models found:", list_data)
        return "AI service is currently unavailable"

    # Step 3: Call the model
    url = f"https://generativelanguage.googleapis.com/v1/{model_name}:generateContent?key={GEMINI_API_KEY}"
    headers = {"Content-Type": "application/json"}
    data = {"contents": [{"parts": [{"text": question}]}]}

    try:
        response = requests.post(url, headers=headers, json=data)
        result = response.json()
        print("Full API response:", result)

        return result["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        print("Error generating content:", e)
        return "AI did not return a response"
