import os
import requests

# -------------------------------
# Set your Gemini API key in environment variables
# -------------------------------
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# -------------------------------
# Define your office services
# -------------------------------
SERVICES = {
    "resident_registration": (
        "We register residents in our woreda and provide them an ID card. "
        "This ID is required to access other services in our office."
    ),
    "birth_certificate": (
        "We issue birth certificates to residents who do not have one. "
        "Requirements: must be a resident of this woreda, must have an ID card, and complete the necessary forms."
    ),
    "marriage_certificate": (
        "We provide marriage certificates. "
        "Requirements: at least one of the couple (bride or groom) must be a resident of the woreda."
    ),
    "divorce_certificate": (
        "We provide divorce certificates following legal procedures. "
        "At least one party must be a resident of this woreda."
    ),
    "death_certificate": (
        "We provide death certificates for residents who have passed away in this woreda. "
        "At least one family member must be a resident and provide necessary documents."
    )
}

# -------------------------------
# Build prompt for AI
# -------------------------------
def build_prompt(question):
    service_descriptions = "\n".join(f"{k}: {v}" for k, v in SERVICES.items())
    prompt = f"""
You are an assistant for our civil registration office. Only answer questions related to the services we provide.
Do not answer anything unrelated. Here are our services:

{service_descriptions}

User question: {question}

Answer concisely and accurately based on our services.
"""
    return prompt

# -------------------------------
# Main AI request function
# -------------------------------
def ask_ai(question):
    if not GEMINI_API_KEY:
        return "Gemini API key is missing"

    prompt = build_prompt(question)

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

    # Step 3: Call the AI model
    url = f"https://generativelanguage.googleapis.com/v1/{model_name}:generateContent?key={GEMINI_API_KEY}"
    headers = {"Content-Type": "application/json"}
    data = {"contents": [{"parts": [{"text": prompt}]}]}

    try:
        response = requests.post(url, headers=headers, json=data)
        result = response.json()
        print("Full API response:", result)

        # Return AI-generated answer
        return result["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        print("Error generating content:", e)
        return "AI did not return a response"

# -------------------------------
# Example usage
# -------------------------------
if __name__ == "__main__":
    question = "How can I get a birth certificate?"
    answer = ask_ai(question)
    print("AI answer:", answer)
