import os
import logging
import asyncio
from dotenv import load_dotenv
from openai import AsyncOpenAI
from openai import RateLimitError
from openai import InternalServerError
from openai import APIStatusError

from tenacity import retry
from tenacity import wait_exponential
from tenacity import stop_after_attempt
from tenacity import retry_if_exception


load_dotenv()

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


client = AsyncOpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)


def should_retry(error):

    if isinstance(error, RateLimitError):
        return True

    if isinstance(error, InternalServerError):
        return True

    if isinstance(error, APIStatusError):
        return error.status_code >= 500

    return False


def log_retry(retry_state):

    attempt = retry_state.attempt_number

    wait_time = retry_state.next_action.sleep

    logger.warning(
        f"Attempt {attempt} failed. "
        f"Waiting {wait_time} seconds"
    )

    print(f"Retry attempt: {attempt}")

    print(f"Wait time: {wait_time} seconds")


@retry(
    wait=wait_exponential(
        multiplier=1,
        min=1,
        max=10
    ),
    stop=stop_after_attempt(5),
    retry=retry_if_exception(should_retry),
    before_sleep=log_retry,
    reraise=True
)
async def ask_model(prompt):

    response = await client.chat.completions.create(
        model=os.getenv(
            "OPENROUTER_MODEL",
            "openrouter/free"
        ),
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content

async def run_one_question(prompt):

    try:
        answer = await ask_model(prompt)

        print("Question:", prompt)
        print("Answer:", answer)

        return answer

    except Exception as error:

        print("Failed:", prompt)
        print("Error:", error)

        return None


async def run_sequential(questions):

    import time

    start_time = time.perf_counter()

    results = []

    for question in questions:

        result = await run_one_question(question)

        results.append(result)

    end_time = time.perf_counter()

    total_time = end_time - start_time

    print("Sequential time:", total_time)

    return results


async def run_concurrent(questions):

    import time

    semaphore = asyncio.Semaphore(3)

    async def limited_question(question):

        async with semaphore:
            return await run_one_question(question)

    start_time = time.perf_counter()

    results = await asyncio.gather(
        *(limited_question(q) for q in questions)
    )

    total_time = time.perf_counter() - start_time

    print("Concurrent time:", total_time)

    return results


async def main():

    questions = [
        "What is Python?",
        "What is AI?",
        "What is machine learning?",
        "What is deep learning?",
        "What is an API?",
        "What is FastAPI?",
        "What is an LLM?",
        "What is RAG?",
        "What is a token?",
        "What is embedding?"
    ]

    print("\n--- SEQUENTIAL ---")

    await run_sequential(questions)

    print("\n--- CONCURRENT ---")

    await run_concurrent(questions)


if __name__ == "__main__":
    asyncio.run(main())