from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

class ItemStatus(str, Enum):
    AVAILABLE = "Disponível"
    RESERVED = "Reservado"
    DONATED = "Doado"
    CANCELLED = "Cancelado"

class ItemCategory(str, Enum):
    ELECTRONICS = "Eletrônicos"
    CLOTHING = "Roupas"
    BOOKS = "Livros"
    FURNITURE = "Mobília"
    TOYS = "Brinquedos"
    SPORTS = "Esportes"
    OTHER = "Outros"

class ItemBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    description: str = Field(..., min_length=10, max_length=1000)
    category: ItemCategory
    condition: str = Field(..., description="Estado do item (novo, usado, etc.)")
    location: str = Field(..., description="Localização do item")
    donor_contact: str = Field(..., description="Contato do doador")

class ItemCreate(ItemBase):
    pass

class ItemUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=100)
    description: Optional[str] = Field(None, min_length=10, max_length=1000)
    category: Optional[ItemCategory] = None
    condition: Optional[str] = None
    location: Optional[str] = None
    status: Optional[ItemStatus] = None

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