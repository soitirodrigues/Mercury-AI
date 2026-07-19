import os
from openai import OpenAI

# Lê a chave da variável de ambiente
api_key = os.getenv("OPENROUTER_API_KEY")

if not api_key:
    raise Exception("OPENROUTER_API_KEY não encontrada.")

print("API encontrada:", api_key[:15] + "...")

# Cliente OpenRouter
client = OpenAI(
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1",
)

# Pergunta ao modelo
response = client.chat.completions.create(
    model="google/gemma-4-26b-a4b-it:free",
    messages=[
        {
            "role": "system",
            "content": (
                "Você é Mercury AI, um especialista em análise de mercado financeiro "
                "e programação Python."
            ),
        },
        {
            "role": "user",
            "content": (
                "Explique em duas linhas o que é Price Action."
            ),
        },
    ],
)

print("\nResposta:")
print(response.choices[0].message.content)
