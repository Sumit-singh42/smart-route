from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    GROQ_API_KEY: Optional[str] = None
    OPENAI_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None
    GEMINI_API_KEY: Optional[str] = None
    
    # Feature Flags
    USE_MOCK_LLM: bool = False # Set to True to save money/quota

    REDIS_URL: str = "redis://redis:6379"
    QDRANT_URL: str = "http://qdrant:6333"
    LM_STUDIO_URL: str = "http://localhost:1234/v1"

    class Config:
        env_file = ".env"

settings = Settings()
