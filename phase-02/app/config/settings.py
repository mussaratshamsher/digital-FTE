from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    GROQ_API_KEY: str
    DATABASE_URL: str
    JWT_SECRET: str
    SUPABASE_URL: str
    SUPABASE_KEY: str
    MODEL_NAME: str = "llama-3.3-70b-versatile"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
