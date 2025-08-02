from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.user_schema import Token, UserLogin
from app.core.deps import get_session
from app.services.auth_service import AuthService

router = APIRouter()

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_session)):
    user = await AuthService.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    access_token = AuthService.create_access_token_for_user(user)
    return {"access_token": access_token, "token_type": "bearer"}

