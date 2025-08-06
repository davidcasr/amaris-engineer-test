from typing import List, Optional
from botocore.exceptions import ClientError
from app.database.client import db_client
from app.models.fund import Fund
import logging

logger = logging.getLogger(__name__)

class FundService:
    """Servicio para gestión de fondos"""
    
    def __init__(self):
        self.table = db_client.get_table("Funds")
    
    async def get_all_funds(self) -> List[Fund]:
        """Obtener todos los fondos disponibles"""
        try:
            response = self.table.scan()
            funds_data = response.get('Items', [])
            
            # Convertir datos de DynamoDB a modelos Pydantic
            funds = []
            for fund_data in funds_data:
                fund = Fund(
                    fundId=fund_data['fundId'],
                    name=fund_data['name'],
                    category=fund_data['category'],
                    minAmount=fund_data['minAmount']
                )
                funds.append(fund)
            
            logger.info(f"Retrieved {len(funds)} funds")
            return funds
            
        except ClientError as e:
            logger.error(f"Error retrieving funds: {str(e)}")
            raise Exception(f"Error al obtener fondos: {str(e)}")
    
    async def get_fund_by_id(self, fund_id: str) -> Optional[Fund]:
        """Obtener un fondo específico por ID"""
        try:
            response = self.table.get_item(Key={'fundId': fund_id})
            
            if 'Item' not in response:
                return None
            
            fund_data = response['Item']
            fund = Fund(
                fundId=fund_data['fundId'],
                name=fund_data['name'],
                category=fund_data['category'],
                minAmount=fund_data['minAmount']
            )
            
            logger.info(f"Retrieved fund: {fund_id}")
            return fund
            
        except ClientError as e:
            logger.error(f"Error retrieving fund {fund_id}: {str(e)}")
            raise Exception(f"Error al obtener fondo {fund_id}: {str(e)}")
    
    async def fund_exists(self, fund_id: str) -> bool:
        """Verificar si un fondo existe"""
        fund = await self.get_fund_by_id(fund_id)
        return fund is not None

# Instancia global del servicio
fund_service = FundService() 