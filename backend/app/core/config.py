from typing import Literal, Optional
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
    METRIC_VERSION: str = "v1.0.0"
    MODEL_REGISTRY_MODE: Literal["mock", "local", "remote"] = "mock"

    # kbo-data ingestion settings
    KBO_DATA_ENABLED: bool = False
    KBO_CHROMEDRIVER_PATH: Optional[str] = None
    KBO_INGESTION_MODE: Literal["mock", "kbo-data"] = "mock"
    KBO_REQUEST_DELAY_SECONDS: float = 1.0
    KBO_RAW_PAYLOAD_DIR: str = "data/raw/kbo"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
