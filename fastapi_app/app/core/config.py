from pydantic import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    """Application settings"""

    # MongoDB settings
    MONGODB_URL: str = os.getenv(
        "MONGODB_URL", 
        "mongodb+srv://backend_user:Ecell@2025@cluster0.blyrgyf.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    )
    DATABASE_NAME: str = os.getenv("DATABASE_NAME", "recruitment_portal")

    # Application settings
    APP_NAME: str = os.getenv("APP_NAME", "Recruitment Portal")
    APP_VERSION: str = os.getenv("APP_VERSION", "1.0.0")
    API_PREFIX: str = os.getenv("API_PREFIX", "/api")

    # Server settings
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))

    # JWT settings
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-replace-in-production")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

    # Environment
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")

    class Config:
        env_file = ".env"
        case_sensitive = True


# Create global settings object
settings = Settings()
