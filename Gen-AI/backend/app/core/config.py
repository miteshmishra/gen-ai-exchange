from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os
from typing import Literal

load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = "Travel Hub"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    DATABASE_URL: str = "sqlite:///./travel_hub.db"
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours
    
    # AI Model Configuration
    AI_PROVIDER: Literal["openai", "ollama"] = os.getenv("AI_PROVIDER", "openai")
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "llama2")

    class Config:
        case_sensitive = True

settings = Settings()
