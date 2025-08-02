from typing import ClassVar
from pydantic_settings import BaseSettings
from sqlalchemy.ext.declarative import declarative_base
import secrets

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    DB_URL: str = "postgresql+asyncpg://postgres:admin@localhost:5432/AchadoseDoados"
    DBBaseModel: ClassVar = declarative_base()

    SECRET_KEY: str = secrets.token_urlsafe(32)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()

