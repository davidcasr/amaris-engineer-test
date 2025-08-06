from typing import Optional
from botocore.exceptions import ClientError
from app.database.client import db_client
from app.models.user import User, UserCreate
from decimal import Decimal
import logging

logger = logging.getLogger(__name__)

class UserService:
    """Servicio para gestión de usuarios"""
    
    def __init__(self):
        self.table = db_client.get_table("User")
    
    async def get_user_by_id(self, user_id: str) -> Optional[User]:
        """Obtener un usuario por ID"""
        try:
            response = self.table.get_item(Key={'userId': user_id})
            
            if 'Item' not in response:
                return None
            
            user_data = response['Item']
            user = User(
                userId=user_data['userId'],
                balance=user_data['balance'],
                notificationType=user_data['notificationType']
            )
            
            logger.info(f"Retrieved user: {user_id}")
            return user
            
        except ClientError as e:
            logger.error(f"Error retrieving user {user_id}: {str(e)}")
            raise Exception(f"Error al obtener usuario {user_id}: {str(e)}")
    
    async def create_user(self, user_data: UserCreate) -> User:
        """Crear un nuevo usuario"""
        try:
            # Verificar si el usuario ya existe
            existing_user = await self.get_user_by_id(user_data.userId)
            if existing_user:
                raise Exception(f"El usuario {user_data.userId} ya existe")
            
            # Crear nuevo usuario
            item = {
                'userId': user_data.userId,
                'balance': user_data.balance,
                'notificationType': user_data.notificationType
            }
            
            self.table.put_item(Item=item)
            
            # Retornar el usuario creado
            created_user = User(**item)
            logger.info(f"Created user: {user_data.userId}")
            return created_user
            
        except ClientError as e:
            logger.error(f"Error creating user {user_data.userId}: {str(e)}")
            raise Exception(f"Error al crear usuario {user_data.userId}: {str(e)}")
    
    async def update_user_balance(self, user_id: str, new_balance: Decimal) -> User:
        """Actualizar el saldo de un usuario"""
        try:
            # Verificar que el usuario existe
            user = await self.get_user_by_id(user_id)
            if not user:
                raise Exception(f"Usuario {user_id} no encontrado")
            
            # Actualizar saldo
            response = self.table.update_item(
                Key={'userId': user_id},
                UpdateExpression='SET balance = :balance',
                ExpressionAttributeValues={':balance': new_balance},
                ReturnValues='ALL_NEW'
            )
            
            updated_data = response['Attributes']
            updated_user = User(
                userId=updated_data['userId'],
                balance=updated_data['balance'],
                notificationType=updated_data['notificationType']
            )
            
            logger.info(f"Updated balance for user {user_id}: {new_balance}")
            return updated_user
            
        except ClientError as e:
            logger.error(f"Error updating balance for user {user_id}: {str(e)}")
            raise Exception(f"Error al actualizar saldo del usuario {user_id}: {str(e)}")
    
    async def update_notification_type(self, user_id: str, notification_type: str) -> User:
        """Actualizar el tipo de notificación de un usuario"""
        try:
            # Verificar que el usuario existe
            user = await self.get_user_by_id(user_id)
            if not user:
                raise Exception(f"Usuario {user_id} no encontrado")
            
            # Validar tipo de notificación
            if notification_type not in ["email", "sms"]:
                raise Exception(f"Tipo de notificación inválido: {notification_type}")
            
            # Actualizar tipo de notificación
            response = self.table.update_item(
                Key={'userId': user_id},
                UpdateExpression='SET notificationType = :notificationType',
                ExpressionAttributeValues={':notificationType': notification_type},
                ReturnValues='ALL_NEW'
            )
            
            updated_data = response['Attributes']
            updated_user = User(
                userId=updated_data['userId'],
                balance=updated_data['balance'],
                notificationType=updated_data['notificationType']
            )
            
            logger.info(f"Updated notification type for user {user_id}: {notification_type}")
            return updated_user
            
        except ClientError as e:
            logger.error(f"Error updating notification type for user {user_id}: {str(e)}")
            raise Exception(f"Error al actualizar tipo de notificación del usuario {user_id}: {str(e)}")
    
    async def user_exists(self, user_id: str) -> bool:
        """Verificar si un usuario existe"""
        user = await self.get_user_by_id(user_id)
        return user is not None

# Instancia global del servicio
user_service = UserService() 