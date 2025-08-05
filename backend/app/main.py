from fastapi import FastAPI
from dotenv import load_dotenv
from app.routes import health

# Cargar variables de entorno
load_dotenv()

# Crear la aplicación FastAPI
app = FastAPI(
    title="Plataforma de Fondos API",
    description="API REST para gestionar fondos de inversión",
    version="1.0.0"
)

# Incluir rutas
app.include_router(health.router, prefix="/api/v1", tags=["health"]) 