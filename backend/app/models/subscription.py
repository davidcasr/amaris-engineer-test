from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from enum import Enum

class SubscriptionErrorCode(Enum):
    """Códigos de error para operaciones de suscripción"""
    USER_NOT_FOUND = ("USER_NOT_FOUND", 404)
    FUND_NOT_FOUND = ("FUND_NOT_FOUND", 404) 
    ALREADY_SUBSCRIBED = ("ALREADY_SUBSCRIBED", 409)
    INSUFFICIENT_BALANCE = ("INSUFFICIENT_BALANCE", 400)
    NOT_SUBSCRIBED = ("NOT_SUBSCRIBED", 400)
    INVALID_REQUEST = ("INVALID_REQUEST", 400)
    INTERNAL_ERROR = ("INTERNAL_ERROR", 500)

class SubscriptionError(BaseModel):
    """Modelo para errores en operaciones de suscripción"""
    code: str = Field(..., description="Código del error")
    status_code: int = Field(..., description="Código HTTP correspondiente")
    message: str = Field(..., description="Mensaje descriptivo del error")
    details: dict = Field(default_factory=dict, description="Detalles adicionales del error")
    
    @classmethod
    def from_code(cls, error_code: SubscriptionErrorCode, message: str, details: dict = None):
        """Crear SubscriptionError desde un SubscriptionErrorCode"""
        return cls(
            code=error_code.value[0],
            status_code=error_code.value[1],
            message=message,
            details=details or {}
        )
    
    class Config:
        json_schema_extra = {
            "example": {
                "code": "USER_NOT_FOUND",
                "status_code": 404,
                "message": "Usuario user123 no encontrado",
                "details": {"userId": "user123"}
            }
        }

class UserFund(BaseModel):
    """Modelo para la relación usuario-fondo (suscripciones activas)"""
    userId: str = Field(..., description="ID del usuario")
    fundId: str = Field(..., description="ID del fondo")
    subscribedAt: datetime = Field(..., description="Fecha de vinculación")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
        json_schema_extra = {
            "example": {
                "userId": "user123",
                "fundId": "FPV_BTG_PACTUAL",
                "subscribedAt": "2025-08-05T10:30:00"
            }
        }

class SubscribeRequest(BaseModel):
    """Modelo para solicitud de suscripción a un fondo"""
    userId: str = Field(..., description="ID del usuario que se suscribe")
    fundId: str = Field(..., description="ID del fondo al que se suscribe")
    
    class Config:
        json_schema_extra = {
            "example": {
                "userId": "user123",
                "fundId": "FPV_BTG_PACTUAL"
            }
        }

class UnsubscribeRequest(BaseModel):
    """Modelo para solicitud de cancelación de suscripción"""
    userId: str = Field(..., description="ID del usuario que cancela")
    fundId: str = Field(..., description="ID del fondo que cancela")
    
    class Config:
        json_schema_extra = {
            "example": {
                "userId": "user123",
                "fundId": "FPV_BTG_PACTUAL"
            }
        }

class SubscriptionResponse(BaseModel):
    """Modelo de respuesta para operaciones de suscripción"""
    success: bool = Field(..., description="Indica si la operación fue exitosa")
    message: str = Field(..., description="Mensaje descriptivo de la operación")
    userFund: Optional[UserFund] = Field(None, description="Detalles de la suscripción")
    error: Optional[SubscriptionError] = Field(None, description="Detalles del error si la operación falló")
    
    class Config:
        json_schema_extra = {
            "examples": [
                {
                    "name": "Successful subscription",
                    "value": {
                        "success": True,
                        "message": "Suscripción exitosa al fondo FPV_BTG_PACTUAL",
                        "userFund": {
                            "userId": "user123",
                            "fundId": "FPV_BTG_PACTUAL",
                            "subscribedAt": "2025-08-05T10:30:00"
                        },
                        "error": None
                    }
                },
                {
                    "name": "Failed subscription",
                    "value": {
                        "success": False,
                        "message": "Usuario user123 no encontrado",
                        "userFund": None,
                        "error": {
                            "code": "USER_NOT_FOUND",
                            "status_code": 404,
                            "message": "Usuario user123 no encontrado",
                            "details": {"userId": "user123"}
                        }
                    }
                }
            ]
        } 