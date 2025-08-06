from pydantic import BaseModel, Field
from typing import Literal
from decimal import Decimal
from app.config import INITIAL_AMOUNT

class User(BaseModel):
    """Modelo para usuarios del sistema"""
    userId: str = Field(..., description="ID único del usuario")
    balance: Decimal = Field(..., ge=0, description="Saldo disponible del usuario")
    notificationType: Literal["email", "sms"] = Field(..., description="Tipo de notificación preferida")
    
    class Config:
        json_encoders = {
            Decimal: float
        }
        json_schema_extra = {
            "example": {
                "userId": "user123",
                "balance": float(INITIAL_AMOUNT),
                "notificationType": "email"
            }
        }

class UserCreate(BaseModel):
    """Modelo para crear un nuevo usuario"""
    userId: str = Field(..., description="ID único del usuario")
    balance: Decimal = Field(INITIAL_AMOUNT, ge=0, description="Saldo inicial del usuario")
    notificationType: Literal["email", "sms"] = Field("email", description="Tipo de notificación preferida")
    
    class Config:
        json_encoders = {
            Decimal: float
        } 