import os
from google import genai

api_key = os.getenv("GEMINI_API_KEY")

print("API encontrada:", api_key[:10], "...")

client = genai.Client(api_key=api_key)

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Diga apenas: Olá Mercury!"
)

print(response.text)