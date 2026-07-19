from functools import lru_cache

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    apifreellm_api_key: str = Field(alias="APIFREELLM_API_KEY")

    endpoint: str = "https://apifreellm.com/api/v1/chat"

    host: str = "0.0.0.0"

    port: int = 8000

    model_name: str = "apifreellm"

    timeout: int = 60

    rate_limit_seconds: float = 25.0

    class Config:
        extra = "ignore"


@lru_cache
def get_settings():
    return Settings()