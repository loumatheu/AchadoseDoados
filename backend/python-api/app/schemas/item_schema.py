from typing import Optional
from pydantic import BaseModel as SCBaseModel

from app.models.item import ItemCategory, ItemStatus, ItemCondition

# Dá pra definir vários schemas de validação para o mesmo modelo SQLAlchemy
class ItemSchema(SCBaseModel):
    id: Optional[int]
    title: str
    description: str
    category: ItemCategory
    item_status: ItemStatus
    condition: ItemCondition
    location: str
    donor_contact: str
    donor_id: int
    recipient_id: Optional[int] = None
    
    class Config:
        orm_mode = True