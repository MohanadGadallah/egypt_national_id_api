from functools import lru_cache
import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application configuration settings loaded from environment variables or .env file.

    Example usage:
        settings = Settings()
        print(settings.DATABASE_URL)


    Environment variable example:
        DATABASE_URL=postgresql+asyncpg://username:password@10.444.55:6666/databasename

    Args:
        BaseSettings (pydantic.BaseSettings): Pydantic base class for settings management.
    """

    DATABASE_URL: str
    TEST_DATABASE_URL: str

    model_config = SettingsConfigDict(
        env_file="test.env" if os.getenv("TEST_MODE") == "true" else ".env",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """
    Retrieve the application settings as a singleton.

    Returns:
        Settings: The application configuration settings.
    """
    return Settings()


settings: Settings = get_settings()
