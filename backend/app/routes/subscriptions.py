from fastapi import APIRouter, HTTPException
from app.models.subscription import SubscribeRequest, UnsubscribeRequest, SubscriptionResponse
from app.services.subscription_service import subscription_service
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/subscribe", response_model=SubscriptionResponse)
async def subscribe_to_fund(request: SubscribeRequest):
    """
    Suscribir un usuario a un fondo de inversión
    
    Validaciones aplicadas:
    - El usuario debe existir
    - El fondo debe existir
    - El usuario no debe estar ya suscrito al fondo
    - El usuario debe tener saldo suficiente (>= monto mínimo del fondo)
    - Se debita el monto mínimo del saldo del usuario
    - Se registra la transacción
    - Se envía notificación según preferencia del usuario
    
    Args:
        request: Datos de la suscripción (userId, fundId)
        
    Returns:
        SubscriptionResponse: Resultado de la operación de suscripción
        
    Raises:
        HTTPException: 400 para errores de validación, 500 para errores internos
    """
    try:
        result = await subscription_service.subscribe_to_fund(request)
        
        if not result.success:
            # Usar el código de estado HTTP del error
            status_code = result.error.status_code if result.error else 400
            raise HTTPException(
                status_code=status_code,
                detail=result.message
            )
        
        logger.info(f"Successful subscription: {request.userId} to {request.fundId}")
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in subscription process: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error interno del servidor: {str(e)}"
        )

@router.post("/unsubscribe", response_model=SubscriptionResponse)
async def unsubscribe_from_fund(request: UnsubscribeRequest):
    """
    Cancelar la suscripción de un usuario a un fondo de inversión
    
    Validaciones aplicadas:
    - El usuario debe existir
    - El fondo debe existir
    - El usuario debe estar suscrito al fondo
    - Se elimina la suscripción
    - Se registra la transacción de cancelación
    - Se envía notificación según preferencia del usuario
    
    Args:
        request: Datos de la cancelación (userId, fundId)
        
    Returns:
        SubscriptionResponse: Resultado de la operación de cancelación
        
    Raises:
        HTTPException: 400 para errores de validación, 500 para errores internos
    """
    try:
        result = await subscription_service.unsubscribe_from_fund(request)
        
        if not result.success:
            # Usar el código de estado HTTP del error
            status_code = result.error.status_code if result.error else 400
            raise HTTPException(
                status_code=status_code,
                detail=result.message
            )
        
        logger.info(f"Successful unsubscription: {request.userId} from {request.fundId}")
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in unsubscription process: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error interno del servidor: {str(e)}"
        ) 