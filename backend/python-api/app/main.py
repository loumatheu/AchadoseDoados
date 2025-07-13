from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
from pathlib import Path

# Importar rotas
from app.routes import items, users, donations

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

# Servir arquivos estáticos (imagens)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Incluir rotas
app.include_router(items.router, prefix="/api/items", tags=["items"])
app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(donations.router, prefix="/api/donations", tags=["donations"])

# Rota de health check
@app.get("/")
async def root():
    return {"message": "Achados e Doados API está funcionando!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "achados-doados-api"}

# Inicializar dados se necessário
@app.on_event("startup")
async def startup_event():
    # Criar diretórios necessários
    Path("data").mkdir(exist_ok=True)
    Path("static").mkdir(exist_ok=True)
    Path("static/images").mkdir(exist_ok=True)
    
    # Inicializar arquivo de dados se não existir
    from app.database.connection import initialize_database
    initialize_database()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)