from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

print("API Key Loaded:", api_key[:10] + "...")

client = genai.Client(api_key=api_key)

print("\nListing Models...")

for model in client.models.list():
    if "gemini-2.0-flash" in model.name:
        print(model.name)

print("\nGenerating...\n")

response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents="Reply with exactly: Hello Govind"
)

print(response.text)