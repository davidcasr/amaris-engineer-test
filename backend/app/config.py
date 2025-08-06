import os
from decimal import Decimal

# Configuración de DynamoDB
DYNAMODB_ENDPOINT = os.getenv("DYNAMODB_ENDPOINT", "http://dynamodb:8000")
AWS_REGION = os.getenv("AWS_REGION", "us-west-2")

# Configuración de ambiente
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
ENABLE_AUTO_DB_INIT = os.getenv("ENABLE_AUTO_DB_INIT", "true").lower() == "true"

# Configuración de negocio
INITIAL_AMOUNT = Decimal("500000")  # COP $500,000 - Monto inicial para nuevos usuarios

def should_auto_initialize_db() -> bool:
    """
    Determinar si se debe auto-inicializar la base de datos
    
    Returns:
        bool: True si se debe inicializar automáticamente, False en caso contrario
    """
    # Nunca en producción (a menos que se force explícitamente)
    if ENVIRONMENT == "production" and not ENABLE_AUTO_DB_INIT:
        return False
    
    # Siempre en desarrollo y test
    if ENVIRONMENT in ["development", "test", "local"]:
        return True
    
    # Por defecto, no auto-inicializar en ambientes desconocidos
    return False 