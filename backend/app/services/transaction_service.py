from typing import List
from botocore.exceptions import ClientError
from app.database.client import db_client
from app.models.transaction import Transaction, TransactionCreate
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class TransactionService:
    """Servicio para gestión de transacciones"""
    
    def __init__(self):
        self.table = db_client.get_table("Transactions")
    
    async def create_transaction(self, transaction_data: TransactionCreate) -> Transaction:
        """Crear una nueva transacción"""
        try:
            # Crear objeto Transaction con ID y timestamp automáticos
            transaction = Transaction(
                userId=transaction_data.userId,
                fundId=transaction_data.fundId,
                type=transaction_data.type,
                amount=transaction_data.amount
            )
            
            # Convertir a diccionario para DynamoDB
            item = {
                'transactionId': transaction.transactionId,
                'userId': transaction.userId,
                'fundId': transaction.fundId,
                'type': transaction.type,
                'amount': transaction.amount,
                'timestamp': transaction.timestamp.isoformat()
            }
            
            # Guardar en DynamoDB
            self.table.put_item(Item=item)
            
            logger.info(f"Created transaction {transaction.transactionId} for user {transaction.userId}")
            return transaction
            
        except ClientError as e:
            logger.error(f"Error creating transaction: {str(e)}")
            raise Exception(f"Error al crear transacción: {str(e)}")
    
    async def get_transactions_by_user(self, user_id: str) -> List[Transaction]:
        """Obtener todas las transacciones de un usuario"""
        try:
            # Usar el índice secundario global para consultar por userId
            response = self.table.query(
                IndexName='UserIdIndex',
                KeyConditionExpression='userId = :userId',
                ExpressionAttributeValues={':userId': user_id},
                ScanIndexForward=False  # Ordenar por timestamp descendente
            )
            
            transactions_data = response.get('Items', [])
            
            # Convertir datos de DynamoDB a modelos Pydantic
            transactions = []
            for transaction_data in transactions_data:
                transaction = Transaction(
                    transactionId=transaction_data['transactionId'],
                    userId=transaction_data['userId'],
                    fundId=transaction_data['fundId'],
                    type=transaction_data['type'],
                    amount=transaction_data['amount'],
                    timestamp=datetime.fromisoformat(transaction_data['timestamp'])
                )
                transactions.append(transaction)
            
            # Ordenar por timestamp descendente (más recientes primero)
            transactions.sort(key=lambda x: x.timestamp, reverse=True)
            
            logger.info(f"Retrieved {len(transactions)} transactions for user {user_id}")
            return transactions
            
        except ClientError as e:
            logger.error(f"Error retrieving transactions for user {user_id}: {str(e)}")
            raise Exception(f"Error al obtener transacciones del usuario {user_id}: {str(e)}")
    
    async def get_transaction_by_id(self, transaction_id: str) -> Transaction:
        """Obtener una transacción específica por ID"""
        try:
            response = self.table.get_item(Key={'transactionId': transaction_id})
            
            if 'Item' not in response:
                raise Exception(f"Transacción {transaction_id} no encontrada")
            
            transaction_data = response['Item']
            transaction = Transaction(
                transactionId=transaction_data['transactionId'],
                userId=transaction_data['userId'],
                fundId=transaction_data['fundId'],
                type=transaction_data['type'],
                amount=transaction_data['amount'],
                timestamp=datetime.fromisoformat(transaction_data['timestamp'])
            )
            
            logger.info(f"Retrieved transaction: {transaction_id}")
            return transaction
            
        except ClientError as e:
            logger.error(f"Error retrieving transaction {transaction_id}: {str(e)}")
            raise Exception(f"Error al obtener transacción {transaction_id}: {str(e)}")

# Instancia global del servicio
transaction_service = TransactionService() 