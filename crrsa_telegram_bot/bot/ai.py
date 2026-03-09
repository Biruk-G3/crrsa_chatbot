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
# Service name translations
# -------------------------------
SERVICE_TRANSLATIONS = {
    "resident_registration": {"am": "የነዋሪ ምዝገባ", "or": "Galmee jiraataa"},
    "birth_certificate": {"am": "የልደት ሰርተፍኬት", "or": "Ragaa dhalootaa"},
    "marriage_certificate": {"am": "የጋብቻ ሰርተፍኬት", "or": "Ragaa gaa'elaa"},
    "divorce_certificate": {"am": "የፍቺ ሰርተፍኬት", "or": "Ragaa hiikkaa gaa'elaa"},
    "death_certificate": {"am": "የሞት ሰርተፍኬት", "or": "Ragaa du'aa"}
}

# -------------------------------
# General civil registration info
# -------------------------------
GENERAL_INFO = {
    "birth_certificate": {
        "en": "A birth certificate is an official record of a person's birth. It is needed for legal identity, school enrollment, and other services.",
        "am": "የልደት ሰርተፍኬት የሰው ልደት መዝገብ ነው። ለሕጋዊ መታወቂያ፣ ትምህርት እና ሌሎች አገልግሎቶች ይኖራል።",
        "or": "Ragaa dhalootaa ragaa seera-qabeessa dhalootaa namaati. Eenyummaa seeraa, barnootaaf, fi tajaajiloota birootti barbaachisa."
    },
    "marriage_certificate": {
        "en": "A marriage certificate proves a legal marriage and is used for administrative purposes.",
        "am": "የጋብቻ ሰርተፍኬት ሕጋዊ ጋብቻን ይማረከዋል።",
        "or": "Ragaa gaa'elaa gaa'ela seeraa ragaa fi tajaajilaaf oola."
    },
    "divorce_certificate": {
        "en": "A divorce certificate is issued after a legal divorce and proves marital status.",
        "am": "የፍቺ ሰርተፍኬት ከሕጋዊ ፍቺ በኋላ ይሰጣል።",
        "or": "Ragaa hiikkaa gaa'elaa fageenya seeraa booda kenname, haala maatii agarsiisa."
    },
    "id_card": {
        "en": "A woreda ID card is an official identity document for residents. Required for access to other civil services.",
        "am": "የወረዳ መታወቂያ ካርድ ለነዋሪዎች የሕጋዊ መታወቂያ ሰነድ ነው።",
        "or": "Kaardii eenyummaa jiraataa seera-qabeessa. Tajaajiloota biroof barbaachisa."
    }
}

# -------------------------------
# Build prompt for AI
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
def ask_ai(question, lang="en"):
    question_lower = question.lower()

    # Service keywords
    KEYWORDS = {
        "resident_registration": ["resident", "registration", "id card", "woreda id"],
        "birth_certificate": ["birth", "birth certificate", "born"],
        "marriage_certificate": ["marriage", "marry", "wedding"],
        "divorce_certificate": ["divorce", "separate", "separation"],
        "death_certificate": ["death", "dead", "funeral"]
    }

    # 1. Check for service-specific question
    for service, words in KEYWORDS.items():
        for word in words:
            if word in question_lower:
                info = SERVICES[service]
                reqs = "\n".join(f"- {r}" for r in info["requirements"])
                if lang == "am":
                    return f"{SERVICE_TRANSLATIONS[service]['am']}\nመስፈርቶች:\n{reqs}"
                if lang == "or":
                    return f"{SERVICE_TRANSLATIONS[service]['or']}\nUlaagaalee:\n{reqs}"
                return f"{info['description']}\nRequirements:\n{reqs}"

    # 2. Check for general info
    for key, info in GENERAL_INFO.items():
        if key in question_lower:
            return info.get(lang, info["en"])

    # 3. Fallback: list services
    if "service" in question_lower or "what do you do" in question_lower:
        service_list = "\n".join(f"- {name.replace('_',' ').title()}" for name in SERVICES.keys())
        if lang == "am":
            return "እኛ የምንሰጣቸው አገልግሎቶች:\n" + service_list
        if lang == "or":
            return "Tajaajiloota nuti kenninu:\n" + service_list
        return f"Our office provides these services:\n{service_list}"

    # 4. If Gemini key missing or general fallback
    if not GEMINI_API_KEY:
        return "I can provide information on resident registration, birth, marriage, divorce, and death certificates."

    # 5. Otherwise, call AI
    prompt = build_prompt(question)
    try:
        list_url = f"https://generativelanguage.googleapis.com/v1/models?key={GEMINI_API_KEY}"
        list_resp = requests.get(list_url)
        list_data = list_resp.json()
        models = list_data.get("models", [])
    except Exception as e:
        print("Error fetching models:", e)
        return "AI service unavailable"

    # Pick compatible model
    model_name = None
    for m in models:
        if "supportedGenerationMethods" in m and "generateContent" in m["supportedGenerationMethods"]:
            model_name = m["name"]
            break
    if not model_name:
        print("No compatible models found:", list_data)
        return "AI service unavailable"

    # Call AI
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
