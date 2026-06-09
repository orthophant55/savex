from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "KBO Insight API"
    APP_ENV: str = "development"
    API_V1_PREFIX: str = "/api/v1"
    FRONTEND_ORIGIN: str = "http://localhost:3000"
    MOCK_MODE: bool = True
    LLM_PROVIDER: str = "mock"
    LLM_API_KEY: Optional[str] = None
    DATABASE_URL: Optional[str] = None
    REDIS_URL: Optional[str] = None

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
