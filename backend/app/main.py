from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from app.routes import health, funds, subscriptions, transactions, settings
from app.database.init import initialize_database
from app.exceptions import *
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Cargar variables de entorno
load_dotenv()

# Crear la aplicación FastAPI
app = FastAPI(
    title="Plataforma de Fondos API",
    description="API REST para gestionar fondos de inversión - Sistema completo de suscripciones",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Incluir todas las rutas
app.include_router(health.router, prefix="/api/v1", tags=["health"])
app.include_router(funds.router, prefix="/api/v1/funds", tags=["funds"])
app.include_router(subscriptions.router, prefix="/api/v1", tags=["subscriptions"])
app.include_router(transactions.router, prefix="/api/v1/transactions", tags=["transactions"])
app.include_router(settings.router, prefix="/api/v1/settings", tags=["settings"])

# Manejadores de errores globales
@app.exception_handler(FundNotFoundException)
async def fund_not_found_handler(request: Request, exc: FundNotFoundException):
    logger.warning(f"Fund not found: {exc.fund_id}")
    return JSONResponse(
        status_code=404,
        content={"error": "Fund not found", "detail": str(exc), "fund_id": exc.fund_id}
    )

@app.exception_handler(UserNotFoundException)
async def user_not_found_handler(request: Request, exc: UserNotFoundException):
    logger.warning(f"User not found: {exc.user_id}")
    return JSONResponse(
        status_code=404,
        content={"error": "User not found", "detail": str(exc), "user_id": exc.user_id}
    )

@app.exception_handler(InsufficientBalanceException)
async def insufficient_balance_handler(request: Request, exc: InsufficientBalanceException):
    logger.warning(f"Insufficient balance: required={exc.required_amount}, current={exc.current_balance}")
    return JSONResponse(
        status_code=400,
        content={
            "error": "Insufficient balance",
            "detail": str(exc),
            "required_amount": exc.required_amount,
            "current_balance": exc.current_balance
        }
    )

@app.exception_handler(AlreadySubscribedException)
async def already_subscribed_handler(request: Request, exc: AlreadySubscribedException):
    logger.warning(f"Already subscribed: user={exc.user_id}, fund={exc.fund_id}")
    return JSONResponse(
        status_code=409,
        content={
            "error": "Already subscribed",
            "detail": str(exc),
            "user_id": exc.user_id,
            "fund_id": exc.fund_id
        }
    )

@app.exception_handler(NotSubscribedException)
async def not_subscribed_handler(request: Request, exc: NotSubscribedException):
    logger.warning(f"Not subscribed: user={exc.user_id}, fund={exc.fund_id}")
    return JSONResponse(
        status_code=400,
        content={
            "error": "Not subscribed",
            "detail": str(exc),
            "user_id": exc.user_id,
            "fund_id": exc.fund_id
        }
    )

@app.exception_handler(InvalidNotificationTypeException)
async def invalid_notification_type_handler(request: Request, exc: InvalidNotificationTypeException):
    logger.warning(f"Invalid notification type: {exc.notification_type}")
    return JSONResponse(
        status_code=400,
        content={
            "error": "Invalid notification type",
            "detail": str(exc),
            "notification_type": exc.notification_type
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": "Ha ocurrido un error interno del servidor",
            "path": str(request.url)
        }
    )

@app.on_event("startup")
async def startup_event():
    """Eventos de inicio de la aplicación"""
    from app.config import ENVIRONMENT, should_auto_initialize_db
    from app.database.client import db_client
    
    logger.info("Starting Plataforma de Fondos API...")
    logger.info(f"Environment detected: {ENVIRONMENT}")
    
    if should_auto_initialize_db():
        logger.info(f"🔧 {ENVIRONMENT.title()} environment - Auto-initializing database...")
        try:
            initialize_database()
            logger.info("✅ Database auto-initialization completed successfully")
        except Exception as e:
            logger.error(f"❌ Database initialization failed: {str(e)}")
            raise
    else:
        logger.info(f"🏭 Production environment detected - Database auto-initialization disabled")
        logger.info("💡 Expecting database to be pre-configured via Infrastructure as Code")
        
        # Solo verificar conectividad en producción
        try:
            if db_client.health_check():
                logger.info("✅ Database connectivity verified successfully")
            else:
                logger.warning("⚠️ Database connectivity check failed")
                raise Exception("Database connectivity verification failed")
        except Exception as e:
            logger.error(f"❌ Database connectivity error: {str(e)}")
            raise

@app.on_event("shutdown")
async def shutdown_event():
    """Eventos de cierre de la aplicación"""
    logger.info("Shutting down Plataforma de Fondos API...")

@app.get("/")
async def root():
    """Endpoint raíz de la API"""
    return {
        "message": "Plataforma de Fondos API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/api/v1/health"
    } 