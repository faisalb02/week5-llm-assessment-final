import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")
BASE_URL = os.getenv("OPENROUTER_BASE_URL")
MODEL = os.getenv("OPENROUTER_MODEL", "openrouter/free")


client = OpenAI(
    api_key=API_KEY,
    base_url=BASE_URL
)


def ask_openai(prompt):

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    answer = response.choices[0].message.content

    print("Answer:", answer)
    print("Model:", response.model)
    print("Usage:", response.usage)

    return response


def ask_claude(prompt, system):

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": system
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    answer = response.choices[0].message.content

    print("Answer:", answer)
    print("Model:", response.model)
    print("Usage:", response.usage)

    return response