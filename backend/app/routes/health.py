from fastapi import APIRouter
from datetime import datetime
import boto3
from app.config import DYNAMODB_ENDPOINT, AWS_REGION

router = APIRouter()

@router.get("/health")
async def health_check():
    """
    Endpoint para verificar el estado del servicio y la conectividad con DynamoDB
    """
    try:
        # Verificar conexión con DynamoDB
        dynamodb = boto3.client(
            'dynamodb',
            endpoint_url=DYNAMODB_ENDPOINT,
            region_name=AWS_REGION,
            aws_access_key_id='dummy',
            aws_secret_access_key='dummy'
        )
        
        # Intentar listar tablas para verificar conectividad
        response = dynamodb.list_tables()
        
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "service": "Plataforma de Fondos API",
            "version": "1.0.0",
            "database": {
                "status": "connected",
                "endpoint": DYNAMODB_ENDPOINT,
                "region": AWS_REGION,
                "tables_count": len(response.get('TableNames', []))
            }
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "timestamp": datetime.now().isoformat(),
            "service": "Plataforma de Fondos API",
            "version": "1.0.0",
            "database": {
                "status": "disconnected",
                "error": str(e),
                "endpoint": DYNAMODB_ENDPOINT,
                "region": AWS_REGION
            }
        } 