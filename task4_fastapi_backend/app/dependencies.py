from openai import AsyncOpenAI

from app.config import settings


def get_settings():
    return settings


def get_llm_client():
    return AsyncOpenAI(
        api_key=settings.OPENROUTER_API_KEY or "test-key",
        base_url="https://openrouter.ai/api/v1"
    )