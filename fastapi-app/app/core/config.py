import os
from pydantic import BaseSettings


class Settings(BaseSettings):
    ENV: str = os.getenv("ENV", "dev")
    DATABASE_URL: str | None = None
    SENTRY_DSN: str | None = None
    # Add other env vars you expect


class Config:
    env_file = ".env"


settings = Settings()