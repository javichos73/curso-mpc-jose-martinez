"""In-memory conversation history — the model 'remembers' because we resend it."""

import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

MODEL = "gemini-2.5-flash"
SYSTEM_INSTRUCTION = "Eres un asistente breve. Respondes en español."

# List of plain dicts, same shape as `contents` — nothing hidden here.
history: list[dict] = []


def send(message: str) -> str:
    history.append({"role": "user", "parts": [{"text": message}]})

    response = client.models.generate_content(
        model=MODEL,
        contents=history,
        config=types.GenerateContentConfig(system_instruction=SYSTEM_INSTRUCTION),
    )

    history.append({"role": "model", "parts": [{"text": response.text}]})
    return response.text


def main() -> None:
    # 8 turns: the fact goes in turn 1, and gets asked back at turn 8.
    print(send("Me llamo Alex y mi color favorito es el verde."))
    print(send("¿Qué framework de Python vimos en la Clase 1?"))
    print(send("Dame un ejemplo de dato que no cabe en un int."))
    print(send("¿Qué hace el comando uv init?"))
    print(send("Explica en una frase qué es un token."))
    print(send("¿Qué significa que una API sea stateless?"))
    print(send("¿Para qué sirve un archivo .env?"))
    print(send("¿Cómo me llamo y cuál es mi color favorito?"))


if __name__ == "__main__":
    main()