from typing import List

from fastapi import APIRouter, status, Depends, HTTPException, Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

# Item imports
from app.models.item import ItemModel
from app.schemas.item_schema import ItemSchema

from app.core.deps import get_session

router = APIRouter()

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=ItemSchema)
async def create_item(item: ItemSchema, db: AsyncSession = Depends(get_session)):
    new_item = ItemModel(
        title = item.title,
        category = item.category,
        description = item.description,
        item_status = item.item_status,
        condition = item.condition,
        location = item.location,
        donor_contact = item.donor_contact,
        donor_id = item.donor_id,
        recipient_id = item.recipient_id if item.recipient_id else None
    ) # tudo isso seria resumido em `ItemModel(**item.dict())`, mas aqui é mais explícito
    
    db.add(new_item)
    
    await db.commit()
    await db.refresh(new_item)
    return new_item

@router.get('/', response_model=List[ItemSchema])
async def get_items(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(ItemModel)
        result = await session.execute(query)
        items: List[ItemModel] = result.scalars().all()
        
        return items

@router.get('/{item_id}', response_model=ItemSchema, status_code=status.HTTP_200_OK)
async def get_item(item_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(ItemModel).where(ItemModel.id == item_id)
        result = await session.execute(query)
        item: ItemModel = result.scalar_one_or_none()
        
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
        
        return item
    
@router.put('/{item_id}', response_model=ItemSchema, status_code=status.HTTP_202_ACCEPTED)
async def update_item(item_id: int, item: ItemSchema, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(ItemModel).where(ItemModel.id == item_id)
        result = await session.execute(query)
        existing_item: ItemModel = result.scalar_one_or_none()
        
        if not existing_item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
        
        for key, value in item.dict().items():
            setattr(existing_item, key, value)
        
        await session.commit()
        await session.refresh(existing_item)
        
        return existing_item
    
@router.delete('/{item_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(ItemModel).where(ItemModel.id == item_id)
        result = await session.execute(query)
        deleted_item = result.scalar_one_or_none()

        if not deleted_item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
        
        await session.delete(deleted_item)
        await session.commit()
        
        return Response(status_code=status.HTTP_204_NO_CONTENT)