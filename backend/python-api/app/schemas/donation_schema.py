from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class DonationCreate(BaseModel):
    item_id: int
    donor_id: int
    recipient_id: Optional[int] = None
    comment: Optional[str] = None


class DonationUpdate(BaseModel):
    recipient_id: Optional[int] = None
    status: Optional[str] = None
    comment: Optional[str] = None


class DonationResponse(BaseModel):
    id: int
    item_id: int
    donor_id: int
    recipient_id: Optional[int]
    date: Optional[datetime]
    status: Optional[str]
    comment: Optional[str]

    class Config:
        orm_mode = True
