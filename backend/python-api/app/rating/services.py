from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func

from typing import List, Optional

from app.rating.models import RatingModel, RatingCreate, RatingResponse, ReputationResponse

class RatingService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_rating(self, rater_id: int, rating_data: RatingCreate) -> RatingResponse:
        """Cria uma nova avaliação no banco de dados."""
        new_rating = RatingModel(
            rater_id=rater_id,
            rated_id=rating_data.rated_id,
            rating=rating_data.rating
        )
        self.db.add(new_rating)
        await self.db.commit()
        await self.db.refresh(new_rating)
        
        return RatingResponse.model_validate(new_rating)

    async def get_user_ratings(self, user_id: int) -> List[RatingResponse]:
        """Obtém todas as avaliações recebidas por um usuário."""
        query = select(RatingModel).where(RatingModel.rated_id == user_id).order_by(RatingModel.created_at.desc())
        result = await self.db.execute(query)
        ratings = result.scalars().all()
        
        return [RatingResponse.model_validate(r) for r in ratings]

    async def get_user_reputation(self, user_id: int) -> ReputationResponse:
        """Calcula a reputação (nota média e total de avaliações) de um usuário."""
        query = select(func.avg(RatingModel.rating), func.count(RatingModel.id)).where(RatingModel.rated_id == user_id)
        result = await self.db.execute(query)
        average_rating, total_ratings = result.one()
        
        return ReputationResponse(
            user_id=user_id,
            average_rating=average_rating if total_ratings > 0 else None,
            total_ratings=total_ratings
        )