from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum as PyEnum

from sqlalchemy import Column, Integer, String, DateTime, Enum

from app.core.configs import settings

# SQLAlchemy model for Item -> modelo de BD
class ItemModel(settings.DBBaseModel):
    __tablename__ = "items"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100), nullable=False)
    category = Column(Enum("Eletrônicos", "Roupas", "Livros", "Mobília", "Brinquedos", "Esportes", "Outros", name="item_category_enum"), nullable=False)
    description = Column(String(1000), nullable=True)
    item_status = Column(Enum("Disponível", "Reservado", "Doado", "Cancelado", name="item_status_enum"), nullable=False)
    condition = Column(Enum("Novo", "Usado", "Recondicionado", name="item_condition_enum"), nullable=False)
    location = Column(String(255), nullable=False)
    donor_contact = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
# Pydantic models for Item -> modelos de validação
class ItemStatus(str, PyEnum):
    AVAILABLE = "Disponível"
    RESERVED = "Reservado"
    DONATED = "Doado"
    CANCELLED = "Cancelado"
    
class ItemCondition(str, PyEnum):
    NEW = "Novo"
    USED = "Usado"
    REFURBISHED = "Recondicionado"

class ItemCategory(str, PyEnum):
    ELECTRONICS = "Eletrônicos"
    CLOTHING = "Roupas"
    BOOKS = "Livros"
    FURNITURE = "Mobília"
    TOYS = "Brinquedos"
    SPORTS = "Esportes"
    OTHER = "Outros"

class ItemBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=100, description="Título do item")
    description: str = Field(..., min_length=10, max_length=1000, description="Descrição do item")
    category: ItemCategory
    item_status: ItemStatus
    condition: str = Field(..., description="Estado do item (novo, usado, etc.)")
    location: str = Field(..., description="Localização do item")
    donor_contact: str = Field(..., description="Contato do doador")

class ItemCreate(ItemBase):
    pass

class ItemUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=100, description="Título do item")
    description: Optional[str] = Field(None, min_length=10, max_length=1000, description="Descrição do item")
    category: Optional[ItemCategory] = None
    status: Optional[ItemStatus] = None
    condition: Optional[str] = None
    location: Optional[str] = None

class ItemResponse(ItemBase):
    id: str
    status: ItemStatus
    created_at: datetime
    updated_at: datetime
    images: List[str] = []
    donor_id: Optional[str] = None
    interested_users: List[str] = []

    class Config:
        from_attributes = True

class ItemFilter(BaseModel):
    category: Optional[ItemCategory] = None
    location: Optional[str] = None
    status: Optional[ItemStatus] = None
    search: Optional[str] = None  # Busca por título ou descrição

class ItemListResponse(BaseModel):
    items: List[ItemResponse]
    total: int
    page: int
    per_page: int
    total_pages: int
