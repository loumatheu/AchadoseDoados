from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum as PyEnum

from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey

from app.core.configs import settings

class DonationModel(settings.DBBaseModel):
    __tablename__ = "donations"
    id = Column(Integer, primary_key=True, autoincrement=True)
    item_id = Column(Integer, ForeignKey("items.id"), nullable=False)
    donor_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    recipient_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    donated_at = Column(DateTime, default=datetime.utcnow)

class DonationBase(BaseModel):
    item_id: int
    donor_id: int
    recipient_id: int
    donated_at: Optional[datetime] = None
