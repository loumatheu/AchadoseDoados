from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from app.core.configs import settings
from app.routes import items, users, donations
from app.routes.geolocation import router as geolocation_router
from app.routes.rating import router as rating_router

# Criar instância do FastAPI
app = FastAPI(
    title="Achados e Doados API",
    description="API para sistema de doação de itens",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especifique os domínios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rotas (url /api/v1/prefix)
app.include_router(items.router, prefix="/items", tags=["items"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(geolocation_router, prefix="/geolocation", tags=["Geolocation"])
app.include_router(rating_router, prefix="/rating", tags=["Rating"])

app.include_router(donations.router, prefix="/api/donations", tags=["donations"])

# Rota de health check
@app.get("/")
async def root():
    return {"message": "Achados e Doados API está funcionando!"}

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True, log_level="info")
