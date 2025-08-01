from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from app.rating.models import RatingCreate, RatingResponse, ReputationResponse
from app.rating.services import RatingService
from app.rating.dependencies import get_rating_service, get_current_user_id

router = APIRouter()

@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=RatingResponse,
    summary="Cria uma nova avaliação",
    description="Permite que um usuário avalie outro com uma nota."
)
async def create_rating_endpoint(
    rating_data: RatingCreate,
    rater_id: int = Depends(get_current_user_id),
    rating_service: RatingService = Depends(get_rating_service)
):
    if rater_id == rating_data.rated_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Você não pode se autoavaliar."
        )
    return await rating_service.create_rating(rater_id, rating_data)

@router.get(
    "/reputation/{user_id}",
    response_model=ReputationResponse,
    summary="Obtém a reputação de um usuário",
    description="Retorna a nota média e o total de avaliações recebidas por um usuário."
)
async def get_reputation_endpoint(
    user_id: int,
    rating_service: RatingService = Depends(get_rating_service)
):
    reputation = await rating_service.get_user_reputation(user_id)
    return reputation

@router.get(
    "/ratings/{user_id}",
    response_model=List[RatingResponse],
    summary="Obtém todas as avaliações de um usuário",
    description="Retorna uma lista de todas as avaliações que um usuário recebeu."
)
async def get_user_ratings_endpoint(
    user_id: int,
    rating_service: RatingService = Depends(get_rating_service)
):
    ratings = await rating_service.get_user_ratings(user_id)
    if not ratings:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nenhuma avaliação encontrada para este usuário.")
    return ratings