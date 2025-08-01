from sqlalchemy import Column, Integer, ForeignKey, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from app.core.database import Base

class DonationModel(Base):
    __tablename__ = "donations"

    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey("items.id"))
    donor_id = Column(Integer, ForeignKey("users.id"))
    recipient_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    date = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="pending")
    comment = Column(String, nullable=True)
    
    item = relationship("ItemModel", back_populates="donations")
    donor = relationship("UserModel", foreign_keys=[donor_id])
    recipient = relationship("UserModel", foreign_keys=[recipient_id])

