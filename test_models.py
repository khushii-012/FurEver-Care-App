import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.getenv("API_KEY")

client = genai.Client(api_key=API_KEY)

response = client.models.generate_content(
    model="gemini-1.5-flash",
    contents="Say hello"
)

print(response.text)