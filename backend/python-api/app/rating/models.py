from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Float
from sqlalchemy.orm import relationship

from app.core.configs import settings
from app.models.user import UserModel 

# SQLAlchemy Model
class RatingModel(settings.DBBaseModel):
    __tablename__ = "ratings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    rater_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    rated_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    rating = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    rater = relationship("UserModel", foreign_keys=[rater_id])
    rated = relationship("UserModel", foreign_keys=[rated_id])

class RatingBase(BaseModel):
    rated_id: int = Field(..., description="ID do usuário a ser avaliado")
    rating: float = Field(..., ge=1.0, le=5.0, description="Nota de 1.0 a 5.0")

class RatingCreate(RatingBase):
    pass

class RatingResponse(RatingBase):
    id: int
    rater_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class ReputationResponse(BaseModel):
    user_id: int
    average_rating: Optional[float]
    total_ratings: int