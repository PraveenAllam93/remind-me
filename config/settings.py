import os
from typing import ClassVar, List

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    """Application settings."""

    API_V1_STR: ClassVar[str] = "/api/v1"
    PROJECT_NAME: ClassVar[str] = "File Processing Service"

    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"

    BACKEND_CORS_ORIGINS: List[str] = ["*"]

    # OpenAI API settings
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_SYSTEM_PROMPT: str = os.getenv(
        "OPENAI_SYSTEM_PROMPT", "You are a helpful assistant."
    )
    TOOL_CALL_MODEL: str = "gpt-4o-mini"
    RESPONSE_MODEL: str = "gpt-4o-mini"

    # Redis settings
    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", "6379"))
    REDIS_DB: int = int(os.getenv("REDIS_DB", "0"))
    REDIS_TASKS_KEY: str = os.getenv("REDIS_TASKS_KEY", "tasks-remind-me")
    REDIS_RESPONSES_ID_KEY: str = os.getenv(
        "REDIS_RESPONSES_ID_KEY", "responses-remind-me"
    )
    REDIS_MAX_RETRIES: int = 3

    # User settings
    DEFAULT_USER_ID: str = "praveenallam"

    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
