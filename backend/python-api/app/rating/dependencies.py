from fastapi import HTTPException, status, Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession
from app.rating.services import RatingService
from app.core.deps import get_session


async def get_rating_service(db: AsyncSession = Depends(get_session)) -> RatingService:
    """
    Retorna uma instância do RatingService com a sessão do banco de dados injetada.
    """
    return RatingService(db=db)

def get_current_user_id(x_user_id: int = Header(..., description="ID do usuário para autenticação")) -> int:
    """
    Dependência temporária que obtém o ID do usuário
    """
    if x_user_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="O ID do usuário fornecido é inválido."
        )
    return x_user_id