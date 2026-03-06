import os
import requests

# -------------------------------
# Gemini API key
# -------------------------------
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# -------------------------------
# Office services with requirements
# -------------------------------
SERVICES = {
    "resident_registration": {
        "description": "We register residents in our woreda and provide them an ID card. This ID is required to access other services in our office.",
        "requirements": ["Must live in the woreda"]
    },
    "birth_certificate": {
        "description": "We issue birth certificates to residents who do not have one.",
        "requirements": [
            "Must be a resident of this woreda",
            "Must have a woreda ID card",
            "Complete necessary forms"
        ]
    },
    "marriage_certificate": {
        "description": "We provide marriage certificates.",
        "requirements": [
            "At least one of the couple (bride or groom) must be a resident of the woreda",
            "Must have a woreda ID card",
            "Complete marriage forms"
        ]
    },
    "divorce_certificate": {
        "description": "We provide divorce certificates following legal procedures.",
        "requirements": [
            "At least one party must be a resident of this woreda",
            "Complete divorce forms"
        ]
    },
    "death_certificate": {
        "description": "We provide death certificates for residents who have passed away in this woreda.",
        "requirements": [
            "At least one family member must be a resident",
            "Provide necessary documents"
        ]
    }
}

# -------------------------------
# Build prompt for AI (if needed)
# -------------------------------
def build_prompt(question):
    service_descriptions = "\n".join(
        f"{k}: {v['description']} Requirements: {', '.join(v['requirements'])}" 
        for k, v in SERVICES.items()
    )
    prompt = f"""
You are an assistant for our civil registration office. Only answer questions related to the services we provide.
Always include exact requirements and conditions for each service when answering.
Do not answer anything unrelated. Here are our services:

{service_descriptions}

User question: {question}

Answer concisely and accurately based on our services.
"""
    return prompt

# -------------------------------
# Main AI function
# -------------------------------
def ask_ai(question):
    question_lower = question.lower()

    # First, match service keywords and return requirements directly
    for key, info in SERVICES.items():
        if key.replace("_", " ") in question_lower or any(word in question_lower for word in key.split("_")):
            reqs = "\n".join(f"- {r}" for r in info["requirements"])
            return f"{info['description']}\nRequirements:\n{reqs}"

    # Fallback to AI if Gemini API key is set
    if not GEMINI_API_KEY:
        return "Gemini API key is missing"

    prompt = build_prompt(question)

    # Step 1: Get models
    try:
        list_url = f"https://generativelanguage.googleapis.com/v1/models?key={GEMINI_API_KEY}"
        list_resp = requests.get(list_url)
        list_data = list_resp.json()
        models = list_data.get("models", [])
    except Exception as e:
        print("Error fetching models:", e)
        return "AI service is currently unavailable"

    # Step 2: Pick first compatible model
    model_name = None
    for m in models:
        if "supportedGenerationMethods" in m and "generateContent" in m["supportedGenerationMethods"]:
            model_name = m["name"]
            break

    if not model_name:
        print("No compatible models found:", list_data)
        return "AI service is currently unavailable"

    # Step 3: Call AI model
    url = f"https://generativelanguage.googleapis.com/v1/{model_name}:generateContent?key={GEMINI_API_KEY}"
    headers = {"Content-Type": "application/json"}
    data = {"contents": [{"parts": [{"text": prompt}]}]}

    try:
        response = requests.post(url, headers=headers, json=data)
        result = response.json()
        print("Full API response:", result)
        return result["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        print("Error generating content:", e)
        return "AI did not return a response"

# -------------------------------
# Example usage
# -------------------------------
if __name__ == "__main__":
    question = "How can I get a marriage certificate?"
    answer = ask_ai(question)
    print("AI answer:", answer)
