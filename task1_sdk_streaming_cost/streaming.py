import time

from .llm_client import client, MODEL


def ask_streaming(prompt):

    start_time = time.time()
    first_token_time = None

    stream = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        stream=True
    )

    print("Streaming response:")

    for chunk in stream:

        content = chunk.choices[0].delta.content

        if content:

            if first_token_time is None:
                first_token_time = time.time()

                elapsed = first_token_time - start_time

                print(
                    f"\nFirst token time: {elapsed:.2f} seconds"
                )

            print(content, end="", flush=True)

    total_time = time.time() - start_time

    print("\n")
    print(f"Total time: {total_time:.2f} seconds")

    return total_time