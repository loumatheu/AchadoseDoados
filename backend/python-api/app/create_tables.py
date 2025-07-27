from app.core.configs import settings
from app.core.database import engine

async def create_tables() -> None:
    """Cria as tabelas no banco de dados"""
    
    import app.models.__all_models
    
    async with engine.begin() as conn:
        # Importar modelos para garantir que sejam registrados
        from app.models.item import ItemModel
        from app.models.user import UserModel
        
        print("Criando tabelas no banco de dados...")
        
        async with engine.begin() as conn:
            await conn.run_sync(settings.DBBaseModel.metadata.drop_all)
            await conn.run_sync(settings.DBBaseModel.metadata.create_all)
        print("Tabelas criadas com sucesso!")
        
if __name__ == "__main__":
    import asyncio
    asyncio.run(create_tables())