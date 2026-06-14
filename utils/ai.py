from google import genai
from google.genai import types

from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

API_KEY = "api_key=API_KEY"


def analyze_pet_health(symptoms):
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

def generate_food_plan(breed, age, weight):
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


def analyze_rescue_case(description, location):
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




def analyze_rescue_image(image, description, location):
    client = genai.Client(api_key=API_KEY)


    prompt = f"""
    You are an emergency animal rescue AI.

    Location: {location}
    Description: {description}

    Analyze the animal and provide:
    1. Injury severity
    2. Condition
    3. Rescue action
    4. Priority level
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




