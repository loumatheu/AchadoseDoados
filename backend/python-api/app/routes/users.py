from typing import List

from fastapi import APIRouter, status, Depends, HTTPException, Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

# User imports
from app.models.user import UserModel
from app.schemas.user_schema import UserSchema

from app.core.deps import get_session

router = APIRouter()

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=UserSchema)
def create_user(user: UserSchema, db: AsyncSession = Depends(get_session)):
    new_user = UserModel(
        username=user.username,
        name=user.name,
        email=user.email,
        password=user.password
    )
    
    db.add(new_user)
    
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get('/', response_model=List[UserSchema])
async def get_users(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UserModel)
        result = await session.execute(query)
        users: List[UserModel] = result.scalars().all()
        
        return users