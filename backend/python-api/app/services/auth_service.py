from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.user import UserModel
from app.core.security import verify_password, hash_password, create_access_token

class AuthService:

    @staticmethod
    async def authenticate_user(db: AsyncSession, username: str, password: str):
        query = select(UserModel).where(UserModel.username == username)
        result = await db.execute(query)
        user = result.scalar_one_or_none()
        if not user:
            return None
        if not verify_password(password, user.password):
            return None
        return user

    @staticmethod
    async def create_user(db: AsyncSession, user_data):
        from app.models.user import UserModel
        new_user = UserModel(
            username=user_data.username,
            name=user_data.name,
            email=user_data.email,
            address=user_data.address,
            phone=user_data.phone,
            password=hash_password(user_data.password),
        )
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        return new_user

    @staticmethod
    def create_access_token_for_user(user):
        return create_access_token(data={"sub": user.username})

