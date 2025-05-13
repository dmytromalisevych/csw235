from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./voting.db"
    ADMIN_USERNAME: str = "admin"
    ADMIN_PASSWORD: str = "admin"  
    SECRET_KEY: str = "your-secret-key-here"  

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()