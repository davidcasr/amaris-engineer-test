from pydantic import BaseModel, Field
from typing import Literal

class NotificationSettingsRequest(BaseModel):
    """Modelo para cambio de configuración de notificaciones"""
    userId: str = Field(..., description="ID del usuario")
    notificationType: Literal["email", "sms"] = Field(..., description="Nuevo tipo de notificación")
    
    class Config:
        schema_extra = {
            "example": {
                "userId": "user123",
                "notificationType": "email"
            }
        }

class NotificationSettingsResponse(BaseModel):
    """Modelo de respuesta para cambio de configuraciones"""
    success: bool = Field(..., description="Indica si la operación fue exitosa")
    message: str = Field(..., description="Mensaje descriptivo de la operación")
    userId: str = Field(..., description="ID del usuario")
    notificationType: str = Field(..., description="Nuevo tipo de notificación configurado")
    
    class Config:
        schema_extra = {
            "example": {
                "success": True,
                "message": "Tipo de notificación actualizado exitosamente",
                "userId": "user123",
                "notificationType": "email"
            }
        } 