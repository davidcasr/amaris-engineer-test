from fastapi import APIRouter, HTTPException, Query
from app.models.transaction import TransactionResponse
from app.services.transaction_service import transaction_service
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/", response_model=TransactionResponse)
async def get_user_transactions(
    userId: str = Query(..., description="ID del usuario para consultar transacciones")
):
    """
    Obtener el historial de transacciones de un usuario
    
    Devuelve todas las transacciones (suscripciones y cancelaciones) del usuario
    ordenadas por fecha de manera descendente (más recientes primero).
    
    Args:
        userId: ID del usuario para consultar sus transacciones
        
    Returns:
        TransactionResponse: Lista de transacciones del usuario con total
        
    Raises:
        HTTPException: 404 si el usuario no existe, 500 para errores internos
    """
    try:
        # Verificar que el usuario existe
        from app.services.user_service import user_service
        user = await user_service.get_user_by_id(userId)
        
        if not user:
            raise HTTPException(
                status_code=404,
                detail=f"Usuario {userId} no encontrado"
            )
        
        # Obtener transacciones del usuario
        transactions = await transaction_service.get_transactions_by_user(userId)
        
        # Crear respuesta
        response = TransactionResponse(
            transactions=transactions,
            total=len(transactions)
        )
        
        logger.info(f"Retrieved {len(transactions)} transactions for user {userId}")
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving transactions for user {userId}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error interno del servidor: {str(e)}"
        ) 