from typing import Optional
from pydantic import BaseModel as SCBaseModel

# Dá pra definir vários schemas de validação para o mesmo modelo SQLAlchemy
class ItemBase(SCBaseModel):
    id: Optional[int]
    title: str
    description: str
    category: str
    item_status: str
    condition: str
    location: str
    donor_contact: str
    
    class Config:
        orm_mode = True