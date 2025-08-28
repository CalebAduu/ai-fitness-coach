from pydantic_settings import BaseSettings
from typing import List
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    supabase_url: str = os.getenv("SUPABASE_URL", "")
    supabase_anon_key: str = os.getenv("SUPABASE_ANON_KEY", "")
    supabase_service_key: str = os.getenv("SUPABASE_SERVICE_KEY", "")
    
    # External API Keys (all free)
    usda_api_key: str = os.getenv("USDA_API_KEY", "")  # Free, just need to register
    exercise_db_api_key: str = os.getenv("EXERCISE_DB_API_KEY", "")  # Free tier
    wger_api_key: str = os.getenv("WGER_API_KEY", "")  # Free, open source
    
    # API Configuration
    api_cache_ttl: int = int(os.getenv("API_CACHE_TTL", 300)) # Cache TTL in seconds
    api_rate_limit: int = int(os.getenv("API_RATE_LIMIT", 10)) # Requests per period
    
    environment: str = os.getenv("ENVIRONMENT", "development")
    debug: bool = os.getenv("DEBUG", "true").lower() == "true"
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    api_host: str = os.getenv("API_HOST", "0.0.0.0")
    api_port: int = int(os.getenv("API_PORT", "8000"))
    cors_origins: List[str] = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")

    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
