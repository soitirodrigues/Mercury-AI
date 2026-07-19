import os
from openai import OpenAI


class MercuryLLM:

    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv("OPENROUTER_API_KEY"),
            base_url="https://openrouter.ai/api/v1"
        )

    def ask(self, prompt: str) -> str:

        response = self.client.chat.completions.create(

            model="google/gemma-4-26b-a4b-it:free",

            messages=[
                {
                    "role": "system",
                    "content": (
                        "Você é o Mercury AI, especialista em Price Action, "
                        "Smart Money Concepts, análise técnica, "
                        "mercado financeiro e trading profissional."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0.2,

            max_tokens=1000,
        )

        return response.choices[0].message.content