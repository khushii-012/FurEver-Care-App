# 1. imports
import os
from dotenv import load_dotenv
from google import genai

# 2. load environment variables
load_dotenv()

# 3. get API key
API_KEY = os.getenv("API_KEY")

# 4. create client
client = genai.Client(api_key=API_KEY)

# 5. test request
response = client.models.generate_content(
    model="gemini-1.5-flash",
    contents="Say hello"
)

print(response.text)