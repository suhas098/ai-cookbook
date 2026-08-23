"""Application configuration, loaded from environment variables.

This is the 12-factor-app pattern: config lives in the environment, not in
code. `.env` is read locally by pydantic-settings; in a real deployment these
same variables would be set by the container runtime / orchestrator.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    app_name: str = "practice-app"
    env: str = "development"
    log_level: str = "info"
    version: str = "0.1.0"
    port: int = 8000


settings = Settings()
