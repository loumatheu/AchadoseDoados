from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum as PyEnum

from sqlalchemy import Column, Integer, String, DateTime, Enum

from app.core.configs import settings

# SQLAlchemy model for Item -> modelo de BD
class UserModel(settings.DBBaseModel):
    __tablename__ = "users"
    
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    username: str = Column(String(50), nullable=False, unique=True)
    name: str = Column(String(100), nullable=False)
    email: str = Column(String(100), nullable=False, unique=True)
    address: str = Column(String(1000), nullable=True)
    phone: str = Column(String(20), nullable=True)
    created_at: datetime = Column(DateTime, default=datetime.utcnow)
    
# Pydantic models for User -> modelos de validação
class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, description="Nome de usuário")
    name: str = Field(..., min_length=3, max_length=100, description="Nome completo")
    email: str = Field(..., min_length=5, max_length=100, description="Email do usuário")
    address: Optional[str] = Field(None, max_length=1000, description="Endereço do usuário")
    phone: Optional[str] = Field(None, max_length=20, description="Telefone do usuário")