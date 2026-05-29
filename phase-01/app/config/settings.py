import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    groq_api_key: str = os.getenv("GROQ_API_KEY", "")
    log_level: str = "INFO"
    model_name: str = "llama-3.3-70b-versatile" # High-performance Groq model

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
