from pydantic import BaseModel, Field
from datetime import datetime
from typing import Literal, List
from decimal import Decimal
import uuid

class Transaction(BaseModel):
    """Modelo para transacciones del sistema"""
    transactionId: str = Field(default_factory=lambda: str(uuid.uuid4()), description="ID único de la transacción")
    userId: str = Field(..., description="ID del usuario")
    fundId: str = Field(..., description="ID del fondo")
    type: Literal["subscribe", "unsubscribe"] = Field(..., description="Tipo de transacción")
    amount: Decimal = Field(..., ge=0, description="Monto de la transacción")
    timestamp: datetime = Field(default_factory=datetime.now, description="Fecha y hora de la transacción")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            Decimal: float
        }
        schema_extra = {
            "example": {
                "transactionId": "550e8400-e29b-41d4-a716-446655440000",
                "userId": "user123",
                "fundId": "FPV_BTG_PACTUAL",
                "type": "subscribe",
                "amount": 75000,
                "timestamp": "2025-08-05T10:30:00"
            }
        }

class TransactionCreate(BaseModel):
    """Modelo para crear una nueva transacción"""
    userId: str = Field(..., description="ID del usuario")
    fundId: str = Field(..., description="ID del fondo")
    type: Literal["subscribe", "unsubscribe"] = Field(..., description="Tipo de transacción")
    amount: Decimal = Field(..., ge=0, description="Monto de la transacción")
    
    class Config:
        json_encoders = {
            Decimal: float
        }

class TransactionResponse(BaseModel):
    """Modelo de respuesta para consulta de transacciones"""
    transactions: List[Transaction] = Field(..., description="Lista de transacciones del usuario")
    total: int = Field(..., description="Número total de transacciones")
    
    class Config:
        schema_extra = {
            "example": {
                "transactions": [
                    {
                        "transactionId": "550e8400-e29b-41d4-a716-446655440000",
                        "userId": "user123",
                        "fundId": "FPV_BTG_PACTUAL",
                        "type": "subscribe",
                        "amount": 75000,
                        "timestamp": "2025-08-05T10:30:00"
                    }
                ],
                "total": 1
            }
        } 