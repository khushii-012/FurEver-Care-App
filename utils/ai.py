from google import genai
from google.genai import types
import os

# ✅ FIX 1: API key seedha env se lo — string "api_key=API_KEY" nahi
API_KEY = os.getenv("GEMINI_API_KEY")


def analyze_pet_health(symptoms):
    try:
        client = genai.Client(api_key=API_KEY)
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
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text

    except Exception as e:
        return f"❌ AI analysis failed: {str(e)}\n\nPlease check your GEMINI_API_KEY in Streamlit secrets."


def generate_food_plan(breed, age, weight):
    try:
        client = genai.Client(api_key=API_KEY)
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
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text

    except Exception as e:
        return f"❌ Food plan generation failed: {str(e)}"


def analyze_rescue_case(description, location):
    try:
        client = genai.Client(api_key=API_KEY)
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
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text

    except Exception as e:
        return f"❌ Rescue analysis failed: {str(e)}"


def analyze_rescue_image(image, description, location):
    try:
        client = genai.Client(api_key=API_KEY)
        prompt = f"""
You are an emergency animal rescue AI.

Location: {location}
Description: {description}

Analyze the animal in the image and provide:
1. Injury severity
2. Animal condition
3. Rescue action needed
4. Priority level (Low / Medium / Critical)
"""
        image_bytes = image.read()

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                prompt,
                types.Part.from_bytes(
                    data=image_bytes,
                    mime_type=image.type
                )
            ]
        )
        return response.text

    except Exception as e:
        return f"❌ Image analysis failed: {str(e)}"