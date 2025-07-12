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

    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
