from typing import List
from fastapi import APIRouter, status, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.donation import DonationModel
from app.models.item import ItemModel
from app.models.user import UserModel

from app.schemas.donation_schema import (
    DonationCreate,
    DonationUpdate,
    DonationResponse
)

from app.core.deps import get_session

router = APIRouter()

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=DonationResponse)
async def create_donation(donation: DonationCreate, db: AsyncSession = Depends(get_session)):
    result = await db.execute(
        select(DonationModel).where(DonationModel.item_id == donation.item_id)
    )
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Este item já foi doado.")

    item_result = await db.execute(select(ItemModel).where(ItemModel.id == donation.item_id))
    if not item_result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Item não encontrado.")

    donor_result = await db.execute(select(UserModel).where(UserModel.id == donation.donor_id))
    if not donor_result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Doador não encontrado.")

    if donation.recipient_id is not None:
        recipient_result = await db.execute(
            select(UserModel).where(UserModel.id == donation.recipient_id)
        )
        if not recipient_result.scalar_one_or_none():
            raise HTTPException(status_code=404, detail="Destinatário não encontrado.")

    new_donation = DonationModel(**donation.dict())

    db.add(new_donation)
    await db.commit()
    await db.refresh(new_donation)

    return new_donation


@router.get('/', response_model=List[DonationResponse])
async def get_donations(db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(DonationModel))
    return result.scalars().all()


@router.get('/{donation_id}', response_model=DonationResponse)
async def get_donation(donation_id: int, db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(DonationModel).where(DonationModel.id == donation_id))
    donation = result.scalar_one_or_none()

    if not donation:
        raise HTTPException(status_code=404, detail="Doação não encontrada.")

    return donation


@router.put('/{donation_id}', response_model=DonationResponse)
async def update_donation(donation_id: int, update_data: DonationUpdate, db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(DonationModel).where(DonationModel.id == donation_id))
    donation = result.scalar_one_or_none()

    if not donation:
        raise HTTPException(status_code=404, detail="Doação não encontrada.")

    for key, value in update_data.dict(exclude_unset=True).items():
        setattr(donation, key, value)

    await db.commit()
    await db.refresh(donation)

    return donation


@router.delete('/{donation_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_donation(donation_id: int, db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(DonationModel).where(DonationModel.id == donation_id))
    donation = result.scalar_one_or_none()

    if not donation:
        raise HTTPException(status_code=404, detail="Doação não encontrada.")

    await db.delete(donation)
    await db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.get('/by-donor/{donor_id}', response_model=List[DonationResponse])
async def get_donations_by_donor(donor_id: int, db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(DonationModel).where(DonationModel.donor_id == donor_id))
    return result.scalars().all()


@router.get('/by-recipient/{recipient_id}', response_model=List[DonationResponse])
async def get_donations_by_recipient(recipient_id: int, db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(DonationModel).where(DonationModel.recipient_id == recipient_id))
    return result.scalars().all()
