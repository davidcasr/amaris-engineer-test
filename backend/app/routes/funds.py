from fastapi import APIRouter, HTTPException
from typing import List
from app.models.fund import Fund
from app.services.fund_service import fund_service
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/", response_model=List[Fund])
async def get_all_funds():
    """
    Obtener todos los fondos disponibles
    
    Returns:
        List[Fund]: Lista de todos los fondos disponibles para suscripción
    """
    try:
        funds = await fund_service.get_all_funds()
        logger.info(f"Retrieved {len(funds)} funds")
        return funds
        
    except Exception as e:
        logger.error(f"Error retrieving funds: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error interno del servidor: {str(e)}"
        )

@router.get("/{fund_id}", response_model=Fund)
async def get_fund_by_id(fund_id: str):
    """
    Obtener información detallada de un fondo específico
    
    Args:
        fund_id: ID del fondo a consultar
        
    Returns:
        Fund: Información detallada del fondo
        
    Raises:
        HTTPException: 404 si el fondo no existe
    """
    try:
        fund = await fund_service.get_fund_by_id(fund_id)
        
        if not fund:
            raise HTTPException(
                status_code=404,
                detail=f"Fondo {fund_id} no encontrado"
            )
        
        logger.info(f"Retrieved fund details for {fund_id}")
        return fund
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving fund {fund_id}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error interno del servidor: {str(e)}"
        ) 