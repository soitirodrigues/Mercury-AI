import os
from openai import OpenAI

# Lê a chave do OpenRouter
api_key = os.getenv("OPENROUTER_API_KEY")

if not api_key:
    raise Exception("OPENROUTER_API_KEY não encontrada.")

# Cria o cliente
client = OpenAI(
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1",
)

def perguntar_llm(pergunta: str) -> str:
    """
    Envia uma pergunta para o modelo e retorna a resposta.
    """

    resposta = client.chat.completions.create(
        model="google/gemma-4-26b-a4b-it:free",
        messages=[
            {
                "role": "system",
                "content": (
                    "Você é um especialista em Price Action, "
                    "Smart Money Concepts, Forex, Ouro, Criptomoedas "
                    "e análise institucional."
                )
            },
            {
                "role": "user",
                "content": pergunta
            }
        ],
        temperature=0.3,
        max_tokens=500,
    )

    return resposta.choices[0].message.content


if __name__ == "__main__":

    pergunta = input("Pergunta: ")

    resposta = perguntar_llm(pergunta)

    print("\nResposta:\n")
    print(resposta)