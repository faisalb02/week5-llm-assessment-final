from fastapi import Depends
from openai import AsyncOpenAI

from app.config import settings
from app.database import database


def get_settings():
    return settings


def get_database():
    return database


def get_llm_client(config=Depends(get_settings)):
    return AsyncOpenAI(
        api_key=config.OPENROUTER_API_KEY or "test-key",
        base_url="https://openrouter.ai/api/v1"
    )