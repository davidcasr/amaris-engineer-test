from pydantic import BaseModel, Field
from typing import Literal
from decimal import Decimal

class Fund(BaseModel):
    """Modelo para fondos de inversión"""
    fundId: str = Field(..., description="ID único del fondo")
    name: str = Field(..., description="Nombre del fondo")
    category: Literal["FPV", "FIC"] = Field(..., description="Categoría del fondo: FPV o FIC")
    minAmount: Decimal = Field(..., gt=0, description="Monto mínimo de suscripción")
    
    class Config:
        json_encoders = {
            Decimal: float
        }
        json_schema_extra = {
            "example": {
                "fundId": "FPV_BTG_PACTUAL",
                "name": "FPV_BTG_PACTUAL",
                "category": "FPV",
                "minAmount": 75000
            }
        } 