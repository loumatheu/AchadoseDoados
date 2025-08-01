from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class DonationSchema(BaseModel):
    id: Optional[int]
    item_id: int
    donor_id: int
    recipient_id: Optional[int] = None
    date: Optional[datetime] = None
    status: Optional[str] = "pending"
    comment: Optional[str] = None

    class Config:
        orm_mode = True

