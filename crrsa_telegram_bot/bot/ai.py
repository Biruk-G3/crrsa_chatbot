import os
import requests

GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")

def ask_ai(question):

    if not question:
        return "Please send a question."

    url = f"https://us-central1-aiplatform.googleapis.com/v1/projects/crrsachatbot/locations/us-central1/publishers/google/models/text-bison-001:predict?key={GOOGLE_API_KEY}"

    payload = {
        "instances": [
            {"content": question}
        ],
        "parameters": {
            "maxOutputTokens": 200
        }
    }

    try:
        response = requests.post(url, json=payload)
        data = response.json()
        print("Full API response:", data)
        if "predictions" in data:
            # Google Vertex AI returns text in this field
            return data["predictions"][0]["content"]
        else:
            return "AI did not return a response."

    except Exception as e:
        return f"Error contacting AI: {str(e)}"