import os
import asyncio

from dotenv import load_dotenv
from openai import AsyncOpenAI

from task3_tools_memory.conversation import Conversation
from task3_tools_memory.tools import (
    TOOL_SCHEMAS,
    execute_tools_parallel
)

load_dotenv()

client = AsyncOpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

MODEL = "openrouter/free"


async def ask_model(messages):

    response = await client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=TOOL_SCHEMAS,
        tool_choice="auto"
    )

    return response.choices[0].message


async def main():

    conversation = Conversation(max_messages=10)

    # Early important information
    conversation.add_message(
        "user",
        "My name is Rahul. My favorite color is blue."
    )

    # 15-turn conversation
    for i in range(15):

        conversation.add_message(
            "user",
            f"Message {i + 1}"
        )

        conversation.add_message(
            "assistant",
            f"Response {i + 1}"
        )

    # Automatic LLM summarization
    await conversation.summarize(client)
    print("Summary contains Rahul:", "Rahul" in conversation.get_summary())

    print("Summary contains blue:", "blue" in conversation.get_summary().lower())

    print("\nAutomatic Summary:")
    print(conversation.get_summary())

    print("\nRecent Messages:")
    print(len(conversation.messages))

    # Summary + recent messages
    final_messages = conversation.get_messages()

    print("\nFinal Memory:")
    print(final_messages)

    # Memory test
    print("\nMemory Test:")

    print(
        "Rahul remembered:",
        any(
            "Rahul" in msg["content"]
            for msg in final_messages
        )
    )

    print(
        "Blue remembered:",
        any(
            "blue" in msg["content"].lower()
            for msg in final_messages
        )
    )


if __name__ == "__main__":
    asyncio.run(main())