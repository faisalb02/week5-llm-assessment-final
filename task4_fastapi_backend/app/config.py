import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    APP_NAME = "Secure Chat API"
    API_KEY = os.getenv("API_KEY", "test-secret-key")
    OPENROUTER_API_KEY = os.getenv(
        "OPENROUTER_API_KEY", ""
    )
    MODEL = os.getenv("MODEL", "openrouter/free")


settings = Settings()