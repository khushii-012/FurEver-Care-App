import os
import requests
from dotenv import load_dotenv

load_dotenv()

def get_api_key():
    key = os.getenv("OPENROUTER_API_KEY")
    if key:
        return key
    try:
        import streamlit as st
        return st.secrets["OPENROUTER_API_KEY"]
    except:
        return None

API_KEY = get_api_key()
API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL   = "mistralai/mistral-7b-instruct:free"  # reliable free model on OpenRouter

def call_ai(prompt):
    try:
        if not API_KEY:
            return "❌ API key not found. Please set OPENROUTER_API_KEY in .env"

        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://furever-care-app.streamlit.app",
            "X-Title": "FurEver Care"
        }
        body = {
            "model": MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 1000
        }
        response = requests.post(API_URL, headers=headers, json=body, timeout=30)

        if response.status_code != 200:
            return f"❌ API Error {response.status_code}: {response.text[:200]}"

        data = response.json()

        # Safe extraction
        if "choices" in data and len(data["choices"]) > 0:
            return data["choices"][0]["message"]["content"]
        elif "error" in data:
            return f"❌ API Error: {data['error'].get('message', str(data['error']))}"
        else:
            return f"❌ Unexpected response: {str(data)[:300]}"

    except requests.exceptions.Timeout:
        return "❌ Request timed out. Please try again."
    except Exception as e:
        return f"❌ AI call failed: {str(e)}"


def analyze_pet_health(symptoms):
    prompt = f"""You are a veterinary AI assistant. Analyze these pet symptoms and give a clear response.

Symptoms: {symptoms}

Provide:
1. Most likely issue
2. Severity (Low / Medium / High)
3. Home care advice
4. Should owner visit vet? (Yes/No and why)

Keep response concise and helpful."""
    return call_ai(prompt)


def generate_food_plan(breed, age, weight):
    prompt = f"""You are a veterinary nutrition expert. Create a food plan for this pet.

Breed: {breed}
Age: {age} years
Weight: {weight} kg

Provide:
1. Daily diet plan (morning/evening)
2. Recommended food items (homemade + commercial brands available in India)
3. Portion sizes
4. Foods strictly to avoid
5. 2-3 health tips

Keep it practical and easy to follow."""
    return call_ai(prompt)


def analyze_rescue_case(description, location):
    prompt = f"""You are an emergency animal rescue AI. Analyze this rescue situation.

Location: {location}
Situation: {description}

Provide a structured rescue report:

🔴 SEVERITY LEVEL: [Low / Medium / Critical]

📋 WHAT HAPPENED:
(Brief assessment of what might be wrong)

🩹 IMMEDIATE FIRST AID STEPS:
(Numbered steps, easy to follow)

🏥 CONTACT HELP:
(Should NGO/Vet be called urgently? Yes/No and why)

⚠️ IMPORTANT WARNINGS:
(What NOT to do)

Keep it clear and actionable for someone on the spot."""
    return call_ai(prompt)


def generate_rescue_report(description, location, ai_analysis):
    prompt = f"""Generate a short formal rescue report for this animal emergency.

Location: {location}
Description: {description}
AI Analysis Summary: {ai_analysis[:500] if ai_analysis else 'Not available'}

Format the report as:
---
FUREVER CARE — ANIMAL RESCUE REPORT
Date: (today)
Location: {location}

INCIDENT SUMMARY:
(2-3 lines)

ANIMAL CONDITION:
(Brief)

RECOMMENDED ACTIONS:
1.
2.
3.

FIRST AID PROVIDED:
(What can be done immediately)

URGENCY LEVEL: [Low/Medium/Critical]
---

Keep it concise, professional, and useful for NGOs/vets."""
    return call_ai(prompt)


def analyze_rescue_image(image, description, location):
    # OpenRouter free tier — use text-based analysis
    prompt = f"""You are an emergency animal rescue AI.

Location: {location}
Description of injured animal: {description}

Based on this description, provide a rescue report:

🔴 SEVERITY LEVEL: [Low / Medium / Critical]

📋 WHAT HAPPENED:
(Assessment based on description)

🩹 IMMEDIATE FIRST AID STEPS:
(Numbered, easy steps for someone on the spot)

🏥 CONTACT HELP:
(Should NGO/Vet be contacted urgently?)

⚠️ DO NOT:
(Common mistakes to avoid)

Keep response clear and actionable."""
    return call_ai(prompt)