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

    # keyword mapping for better detection
    KEYWORDS = {
        "resident_registration": ["resident", "registration", "id card", "woreda id"],
        "birth_certificate": ["birth", "birth certificate", "born"],
        "marriage_certificate": ["marriage", "marry", "wedding"],
        "divorce_certificate": ["divorce", "separate", "separation"],
        "death_certificate": ["death", "dead", "funeral"]
    }

    # detect service using keywords
    for service, words in KEYWORDS.items():
        for word in words:
            if word in question_lower:
                info = SERVICES[service]
                reqs = "\n".join(f"- {r}" for r in info["requirements"])
                return f"{info['description']}\nRequirements:\n{reqs}"

    # handle general questions without AI
    if "service" in question_lower or "what do you do" in question_lower:
        service_list = "\n".join(
            f"- {name.replace('_',' ').title()}" for name in SERVICES.keys()
        )
        return f"Our office provides these services:\n{service_list}"

    # if Gemini key missing
    if not GEMINI_API_KEY:
        return "Please ask about resident registration, birth certificate, marriage certificate, divorce certificate, or death certificate."

    prompt = build_prompt(question)

    # Step 1: get models
    try:
        list_url = f"https://generativelanguage.googleapis.com/v1/models?key={GEMINI_API_KEY}"
        list_resp = requests.get(list_url)
        list_data = list_resp.json()
        models = list_data.get("models", [])
    except Exception as e:
        print("Error fetching models:", e)
        return "AI service unavailable"

    # Step 2: pick compatible model
    model_name = None
    for m in models:
        if "supportedGenerationMethods" in m and "generateContent" in m["supportedGenerationMethods"]:
            model_name = m["name"]
            break

    if not model_name:
        print("No compatible models found:", list_data)
        return "AI service unavailable"

    # Step 3: call AI
    url = f"https://generativelanguage.googleapis.com/v1/{model_name}:generateContent?key={GEMINI_API_KEY}"
    headers = {"Content-Type": "application/json"}
    data = {"contents": [{"parts": [{"text": prompt}]}]}

    try:
        response = requests.post(url, headers=headers, json=data)
        result = response.json()

        if "candidates" in result:
            return result["candidates"][0]["content"]["parts"][0]["text"]

        return "I can help with birth, marriage, divorce, death certificates, and resident registration."

    except Exception as e:
        print("Error generating content:", e)
        return "AI did not return a response"
