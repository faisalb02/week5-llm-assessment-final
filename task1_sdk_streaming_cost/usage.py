import os
import json
from datetime import date
from pathlib import Path

import tiktoken
from dotenv import load_dotenv

load_dotenv()

# Token limit
MAX_INPUT_TOKENS = int(
    os.getenv("MAX_INPUT_TOKENS", 4000)
)

# Pricing per 1 million tokens
INPUT_PRICE = float(
    os.getenv("INPUT_PRICE_PER_1M", 0)
)

OUTPUT_PRICE = float(
    os.getenv("OUTPUT_PRICE_PER_1M", 0)
)

# Tokenizer
encoding = tiktoken.get_encoding("cl100k_base")

# Usage log file
LOG_FILE = Path("logs") / "usage.jsonl"


def count_tokens(messages):

    total_tokens = 0

    for message in messages:

        content = message.get("content", "")

        if isinstance(content, str):
            total_tokens += len(
                encoding.encode(content)
            )

    return total_tokens


def check_token_limit(messages):

    total_tokens = count_tokens(messages)

    if total_tokens > MAX_INPUT_TOKENS:
        raise ValueError(
            f"Token limit exceeded: {total_tokens}"
        )

    return total_tokens


def calculate_cost(input_tokens, output_tokens):

    input_cost = (
        input_tokens / 1_000_000
    ) * INPUT_PRICE

    output_cost = (
        output_tokens / 1_000_000
    ) * OUTPUT_PRICE

    total_cost = input_cost + output_cost

    return round(total_cost, 8)


def log_usage(input_tokens, output_tokens):

    LOG_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    cost = calculate_cost(
        input_tokens,
        output_tokens
    )

    record = {
        "date": date.today().isoformat(),
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": input_tokens + output_tokens,
        "cost": cost
    }

    with open(
        LOG_FILE,
        "a",
        encoding="utf-8"
    ) as file:

        file.write(
            json.dumps(record) + "\n"
        )

    return record


def get_today_usage():

    today = date.today().isoformat()

    total_tokens = 0
    total_cost = 0

    if not LOG_FILE.exists():
        return {
            "date": today,
            "total_tokens": 0,
            "total_cost": 0
        }

    with open(
        LOG_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        for line in file:

            record = json.loads(line)

            if record["date"] == today:

                total_tokens += record["total_tokens"]

                total_cost += record["cost"]

    return {
        "date": today,
        "total_tokens": total_tokens,
        "total_cost": round(total_cost, 8)
    }