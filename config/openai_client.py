from openai import OpenAI

from .settings import settings


def get_openai_client() -> OpenAI:
    """Create and return an OpenAI client instance."""
    return OpenAI(api_key=settings.OPENAI_API_KEY)


openai_client = get_openai_client()
