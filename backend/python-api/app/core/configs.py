from typing import List, ClassVar
from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl
from sqlalchemy.ext.declarative import declarative_base

class Settings(BaseSettings):
    """
    Configurações gerais usadas na aplicação.
    """
    API_V1_STR: str = "/api/v1"
    DB_URL: str = "postgresql+asyncpg://postgres:admin@localhost:5432/AchadoseDoados"          # user:usarname:password
    DBBaseModel: ClassVar = declarative_base()                                                 # user: postgres:admin
    
    class Config:
        case_sensitive = True
        env_file = ".env"
        

settings = Settings()