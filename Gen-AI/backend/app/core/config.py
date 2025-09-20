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
    AI_PROVIDER: Literal["openai", "ollama", "gemini"] = os.getenv("AI_PROVIDER", "openai")
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "llama2")

    # Google Cloud / Vertex AI Configuration
    GOOGLE_CLOUD_PROJECT: str = os.getenv("GOOGLE_CLOUD_PROJECT", "")
    GOOGLE_CLOUD_LOCATION: str = os.getenv("GOOGLE_CLOUD_LOCATION", "")
    GOOGLE_APPLICATION_CREDENTIALS: str = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "")
    ADK_MODEL_ID: str = os.getenv("ADK_MODEL_ID", "gemini-pro")

    class Config:
        case_sensitive = True

    def reload(self):
        # Reload environment variables
        load_dotenv()
        for field in self.model_fields:
            setattr(self, field, os.getenv(field.upper(), getattr(self, field)))

settings = Settings()
