from fastapi import APIRouter, HTTPException, Query, File, UploadFile, Form
from typing import List, Optional
import math
from app.models.item import ItemCreate, ItemResponse, ItemUpdate, ItemFilter, ItemListResponse
from app.services.item_service import ItemService
from app.database.connection import get_database

router = APIRouter()

@router.post("/", response_model=ItemResponse)
async def create_item(item: ItemCreate):
    """Cria um novo item para doação"""
    try:
        db = get_database()
        item_service = ItemService(db)
        created_item = item_service.create_item(item.dict())
        return created_item
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=ItemListResponse)
async def get_items(
    page: int = Query(1, ge=1, description="Número da página"),
    per_page: int = Query(10, ge=1, le=100, description="Itens por página"),
    category: Optional[str] = Query(None, description="Filtrar por categoria"),
    location: Optional[str] = Query(None, description="Filtrar por localização"),
    status: Optional[str] = Query(None, description="Filtrar por status"),
    search: Optional[str] = Query(None, description="Buscar por título ou descrição")
):
    """Lista todos os itens com filtros e paginação"""
    try:
        db = get_database()
        item_service = ItemService(db)
        
        # Criar filtros
        filters = ItemFilter(
            category=category,
            location=location,
            status=status,
            search=search
        )
        
        # Buscar itens
        items = item_service.get_items_with_filters(filters)
        
        # Paginação
        total = len(items)
        total_pages = math.ceil(total / per_page)
        start = (page - 1) * per_page
        end = start + per_page
        paginated_items = items[start:end]
        
        return ItemListResponse(
            items=paginated_items,
            total=total,
            page=page,
            per_page=per_page,
            total_pages=total_pages
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{item_id}", response_model=ItemResponse)
async def get_item(item_id: str):
    """Busca um item específico pelo ID"""
    try:
        db = get_database()
        item_service = ItemService(db)
        item = item_service.get_item(item_id)
        
        if not item:
            raise HTTPException(status_code=404, detail="Item não encontrado")
        
        return item
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{item_id}", response_model=ItemResponse)
async def update_item(item_id: str, item_update: ItemUpdate):
    """Atualiza um item existente"""
    try:
        db = get_database()
        item_service = ItemService(db)
        
        # Verificar se o item existe
        existing_item = item_service.get_item(item_id)
        if not existing_item:
            raise HTTPException(status_code=404, detail="Item não encontrado")
        
        # Atualizar apenas os campos fornecidos
        update_data = item_update.dict(exclude_unset=True)
        updated_item = item_service.update_item(item_id, update_data)
        
        return updated_item
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{item_id}")
async def delete_item(item_id: str):
    """Remove um item"""
    try:
        db = get_database()
        item_service = ItemService(db)
        
        # Verificar se o item existe
        existing_item = item_service.get_item(item_id)
        if not existing_item:
            raise HTTPException(status_code=404, detail="Item não encontrado")
        
        success = item_service.delete_item(item_id)
        if success:
            return {"message": "Item removido com sucesso"}
        else:
            raise HTTPException(status_code=500, detail="Erro ao remover item")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{item_id}/images")
async def upload_item_images(item_id: str, files: List[UploadFile] = File(...)):
    """Upload de imagens para um item"""
    try:
        db = get_database()
        item_service = ItemService(db)
        
        # Verificar se o item existe
        existing_item = item_service.get_item(item_id)
        if not existing_item:
            raise HTTPException(status_code=404, detail="Item não encontrado")
        
        # Processar upload das imagens
        uploaded_images = await item_service.upload_images(item_id, files)
        
        return {
            "message": "Imagens enviadas com sucesso",
            "images": uploaded_images
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{item_id}/interest")
async def express_interest(item_id: str, user_id: str = Form(...)):
    """Expressar interesse em um item"""
    try:
        db = get_database()
        item_service = ItemService(db)
        
        # Verificar se o item existe
        existing_item = item_service.get_item(item_id)
        if not existing_item:
            raise HTTPException(status_code=404, detail="Item não encontrado")
        
        # Verificar se o item está disponível
        if existing_item["status"] != "available":
            raise HTTPException(status_code=400, detail="Item não está disponível")
        
        # Adicionar usuário à lista de interessados
        success = item_service.add_interested_user(item_id, user_id)
        if success:
            return {"message": "Interesse registrado com sucesso"}
        else:
            raise HTTPException(status_code=400, detail="Usuário já demonstrou interesse")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/categories/list")
async def get_categories():
    """Lista todas as categorias disponíveis"""
    from app.models.item import ItemCategory
    return {
        "categories": [
            {"value": cat.value, "label": cat.value.title()}
            for cat in ItemCategory
        ]
    }

@router.get("/stats/summary")
async def get_items_stats():
    """Estatísticas gerais dos itens"""
    try:
        db = get_database()
        item_service = ItemService(db)
        stats = item_service.get_stats()
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))