from app.models.item import Item
from app.core import Session
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.item import ItemModel  # modelo ORM do banco de dados
from schemas import ItemCreate, ItemUpdate, ItemFilter  # seus Pydantic models

def create_item(item: ItemCreate, db: Session = Session) -> ItemModel:
    item = ItemModel(**item.dict)