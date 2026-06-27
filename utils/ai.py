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
MODEL   = "google/gemini-2.0-flash-exp:free"  # free Gemini on OpenRouter

def call_ai(prompt):
    try:
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        body = {
            "model": MODEL,
            "messages": [{"role": "user", "content": prompt}]
        }
        response = requests.post(API_URL, headers=headers, json=body, timeout=30)
        data = response.json()
        return data["choices"][0]["message"]["content"]
    except Exception as e:
        return f"❌ AI call failed: {str(e)}"


def analyze_pet_health(symptoms):
    prompt = f"""
You are a veterinary AI assistant.

Analyze these pet symptoms:
{symptoms}

Give:
1. Possible issue
2. Severity (Low/Medium/High)
3. Care advice
4. Whether vet visit is needed
"""
    return call_ai(prompt)


def generate_food_plan(breed, age, weight):
    prompt = f"""
You are a veterinary nutrition expert AI.

Create a detailed food plan for a pet with:
Breed: {breed}
Age: {age} years
Weight: {weight} kg

Give:
1. Daily diet plan
2. Food items (home + commercial)
3. Quantity guidance
4. Foods to avoid
5. Health tips
"""
    return call_ai(prompt)


def analyze_rescue_case(description, location):
    prompt = f"""
You are an emergency animal rescue AI assistant.

Analyze this situation:
Location: {location}
Description: {description}

Provide:
1. Injury severity (Low / Medium / Critical)
2. What might be wrong with the animal
3. Immediate first aid steps
4. Should NGO / Vet be contacted urgently (Yes/No)
5. Short rescue advice
"""
    return call_ai(prompt)


def analyze_rescue_image(image, description, location):
    # OpenRouter free tier doesn't support image — fallback to text
    prompt = f"""
You are an emergency animal rescue AI.

Location: {location}
Description: {description}

Based on the description, provide:
1. Injury severity (Low / Medium / Critical)
2. Animal condition assessment
3. Immediate rescue action needed
4. Priority level
5. First aid tips
"""
    return call_ai(prompt)