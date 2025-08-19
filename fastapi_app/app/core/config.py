from pydantic import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings"""

    # MongoDB settings
    MONGODB_URL: str = "mongodb+srv://backend_user:Ecell@2025@cluster0.blyrgyf.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    DATABASE_NAME: str = "recruitment_portal"

    # Application settings
    APP_NAME: str = "Recruitment Portal"
    APP_VERSION: str = "1.0.0"
    API_PREFIX: str = "/api"

    # JWT settings
    SECRET_KEY: str = "your-secret-key"  
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"
        case_sensitive = True


# Create global settings object
settings = Settings()
