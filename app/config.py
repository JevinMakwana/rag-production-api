"""
Centralized Configuration
Uses pydantic-settings for validated environment variables.
"""

from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Optional

# Load .env into os.environ so LangChain/LangSmith SDK can read tracing config
load_dotenv()

class Settings(BaseSettings):
    
    # LLM Configuration (Azure OpenAI)
    azure_openai_gpt4omini_endpoint: str
    azure_openai_gpt4omini_deployment: str = "npi-gpt-4" # primary_model
    azure_openai_gpt4omini_api_key: str
    azure_openai_gpt4omini_api_version: str = "2024-02-01"


    # Embedding Configuration (Azure OpenAI)
    azure_openai_emb_endpoint: str
    azure_openai_emb_deployment: str = "npi-text-embedding-ada"
    azure_openai_emb_api_key: str
    azure_openai_emb_api_version: str = "2024-02-01"
    
    # Anthropic (Optional, if needed for fallback)
    anthropic_api_key: Optional[str] = None
    
    # LangSmith
    langchain_tracing_v2: bool = True
    langchain_api_key: str = ""
    langchain_project: str = "production-api"
    
    
    # Application
    app_env: str = "development"
    log_level: str = "INFO"
    rate_limit: str = "20/minute"
    cache_ttl_seconds: int = 300
    max_retries: int = 3
    
    
    model_config = {"env_file": ".env", "extra": "ignore"}
    
    @property
    def is_production(self) -> bool:
        return self.app_env == "production"
    
@lru_cache
def get_settings() -> Settings:
    """Cached settings instance - loaded once, reused everywhere."""
    return Settings()