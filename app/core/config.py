# app/core/config.py

from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):

    # JWT settings
    SECRET_KEY:          str = "your-super-secret-key-change-in-production"
    ALGORITHM:           str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Database settings
    DB_HOST:     str = "localhost"
    DB_PORT:     int = 5432
    DB_NAME:     str = "siem_db"
    DB_USER:     str = "postgres"
    DB_PASSWORD: str = "narale022"

    # Application settings
    APP_NAME:    str = "ARGUS SIEM"
    APP_VERSION: str = "2.0.0"
    DEBUG:       bool = True

    # Detection settings
    BRUTE_FORCE_THRESHOLD: int = 5
    ERROR_STORM_THRESHOLD: int = 3

    # CORS settings
    CORS_ORIGINS: list = ["*"]

    class Config:
        env_file = ".env"
        extra = "allow"

@lru_cache()
def get_settings() -> Settings:
    
    return Settings()

# Single instance used everywhere
settings = get_settings()