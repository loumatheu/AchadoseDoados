from typing import List, Optional

from fastapi import APIRouter, status, Depends, HTTPException, Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

# User imports
from app.models.user import UserModel
from app.schemas.user_schema import UserBase, UserCreate, UserRead, UserLogin, Token, TokenData

from app.core.deps import get_session

from pydantic import BaseModel, EmailStr

router = APIRouter()

class UserUpdate(BaseModel):
    username: Optional[str] = None
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    password: Optional[str] = None


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=UserRead)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_session)):
    new_user = UserModel(
        username=user.username,
        name=user.name,
        email=user.email,
        address=user.address,
        phone=user.phone,
        password=user.password
    )
    
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


@router.get('/', response_model=List[UserRead])
async def get_users(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UserModel)
        result = await session.execute(query)
        users: List[UserModel] = result.scalars().all()
        return users


@router.get('/{user_id}', response_model=UserRead)
async def get_user(user_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UserModel).where(UserModel.id == user_id)
        result = await session.execute(query)
        user: UserModel = result.scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user


@router.put('/{user_id}', response_model=UserRead, status_code=status.HTTP_202_ACCEPTED)
async def update_user(user_id: int, user: UserUpdate, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UserModel).where(UserModel.id == user_id)
        result = await session.execute(query)
        existing_user: UserModel = result.scalar_one_or_none()
        
        if not existing_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        user_data = user.dict(exclude_unset=True)
        for key, value in user_data.items():
            setattr(existing_user, key, value)
        
        await session.commit()
        await session.refresh(existing_user)
        
        return existing_user
    

@router.delete('/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UserModel).where(UserModel.id == user_id)
        result = await session.execute(query)
        deleted_user = result.scalar_one_or_none()

        if not deleted_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
        await session.delete(deleted_user)
        await session.commit()
        
        return Response(status_code=status.HTTP_204_NO_CONTENT)
