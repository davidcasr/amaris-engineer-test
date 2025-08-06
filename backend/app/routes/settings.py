from fastapi import APIRouter, HTTPException
from app.models.settings import NotificationSettingsRequest, NotificationSettingsResponse
from app.services.user_service import user_service
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/notifications", response_model=NotificationSettingsResponse)
async def update_notification_settings(request: NotificationSettingsRequest):
    """
    Cambiar el tipo de notificación del usuario
    
    Permite al usuario cambiar su preferencia de notificación entre "email" y "sms".
    
    Args:
        request: Datos de la nueva configuración (userId, notificationType)
        
    Returns:
        NotificationSettingsResponse: Resultado de la operación de actualización
        
    Raises:
        HTTPException: 404 si el usuario no existe, 400 para datos inválidos, 500 para errores internos
    """
    try:
        # Verificar que el usuario existe
        user = await user_service.get_user_by_id(request.userId)
        
        if not user:
            raise HTTPException(
                status_code=404,
                detail=f"Usuario {request.userId} no encontrado"
            )
        
        # Actualizar tipo de notificación
        updated_user = await user_service.update_notification_type(
            request.userId, 
            request.notificationType
        )
        
        # Crear respuesta exitosa
        response = NotificationSettingsResponse(
            success=True,
            message=f"Tipo de notificación actualizado exitosamente a {request.notificationType}",
            userId=updated_user.userId,
            notificationType=updated_user.notificationType
        )
        
        logger.info(f"Updated notification type for user {request.userId} to {request.notificationType}")
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        # Manejar errores específicos de validación
        if "Tipo de notificación inválido" in str(e):
            raise HTTPException(
                status_code=400,
                detail=str(e)
            )
        
        logger.error(f"Error updating notification settings for user {request.userId}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error interno del servidor: {str(e)}"
        ) 