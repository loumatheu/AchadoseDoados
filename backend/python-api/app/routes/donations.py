from typing import List
from fastapi import APIRouter, status, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.donation import DonationModel
from app.schemas.donation_schema import DonationSchema

from app.core.deps import get_session

router = APIRouter()

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=DonationSchema)
async def create_donation(donation: DonationSchema, db: AsyncSession = Depends(get_session)):
    new_donation = DonationModel(**donation.dict())

    db.add(new_donation)
    await db.commit()
    await db.refresh(new_donation)

    return new_donation

@router.get('/', response_model=List[DonationSchema])
async def get_donations(db: AsyncSession = Depends(get_session)):
    async with db as session:
        result = await session.execute(select(DonationModel))
        donations = result.scalars().all()
        return donations

@router.get('/{donation_id}', response_model=DonationSchema)
async def get_donation(donation_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        result = await session.execute(select(DonationModel).where(DonationModel.id == donation_id))
        donation = result.scalar_one_or_none()

        if not donation:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Donation not found")

        return donation

@router.put('/{donation_id}', response_model=DonationSchema)
async def update_donation(donation_id: int, donation: DonationSchema, db: AsyncSession = Depends(get_session)):
    async with db as session:
        result = await session.execute(select(DonationModel).where(DonationModel.id == donation_id))
        existing_donation = result.scalar_one_or_none()

        if not existing_donation:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Donation not found")

        for key, value in donation.dict().items():
            setattr(existing_donation, key, value)

        await session.commit()
        await session.refresh(existing_donation)

        return existing_donation

@router.delete('/{donation_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_donation(donation_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        result = await session.execute(select(DonationModel).where(DonationModel.id == donation_id))
        existing_donation = result.scalar_one_or_none()

        if not existing_donation:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Donation not found")

        await session.delete(existing_donation)
        await session.commit()

        return Response(status_code=status.HTTP_204_NO_CONTENT)

