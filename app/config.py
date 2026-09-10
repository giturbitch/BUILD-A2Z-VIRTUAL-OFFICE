from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # LLM Configuration
    llm_provider: str = "ollama"  # ollama or anthropic
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama3.1"
    anthropic_api_key: Optional[str] = None

    # API Keys
    ghl_api_key: str
    ghl_location_id: Optional[str] = None

    # Social Media
    instagram_username: Optional[str] = None
    instagram_password: Optional[str] = None
    linkedin_username: Optional[str] = None
    linkedin_password: Optional[str] = None
    twitter_api_key: Optional[str] = None
    twitter_api_secret: Optional[str] = None
    twitter_access_token: Optional[str] = None
    twitter_access_secret: Optional[str] = None

    # Database
    database_url: str = "sqlite:///./agents.db"

    # Server
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    debug: bool = False

    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
