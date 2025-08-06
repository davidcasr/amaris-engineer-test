from typing import List, Optional
from botocore.exceptions import ClientError
from app.database.client import db_client
from app.models.subscription import (
    UserFund, SubscribeRequest, UnsubscribeRequest, SubscriptionResponse,
    SubscriptionError, SubscriptionErrorCode
)
from app.models.transaction import TransactionCreate
from app.services.user_service import user_service
from app.services.fund_service import fund_service
from app.services.transaction_service import transaction_service
from app.services.notification_service import notification_service
from datetime import datetime
from decimal import Decimal
import logging

logger = logging.getLogger(__name__)

class SubscriptionService:
    """Servicio para gestión de suscripciones con lógica de negocio completa"""
    
    def __init__(self):
        self.table = db_client.get_table("UserFunds")
    
    async def subscribe_to_fund(self, request: SubscribeRequest) -> SubscriptionResponse:
        """
        Suscribir un usuario a un fondo con validaciones completas
        
        Reglas de negocio:
        1. El usuario debe existir
        2. El fondo debe existir
        3. El usuario no debe estar ya suscrito al fondo
        4. El usuario debe tener saldo suficiente (>= monto mínimo del fondo)
        5. Se debe debitar el monto mínimo del saldo del usuario
        6. Se debe registrar la transacción
        7. Se debe enviar notificación según preferencia del usuario
        """
        try:
            # 1. Verificar que el usuario existe
            user = await user_service.get_user_by_id(request.userId)
            if not user:
                error = SubscriptionError.from_code(
                    SubscriptionErrorCode.USER_NOT_FOUND,
                    f"Usuario {request.userId} no encontrado",
                    {"userId": request.userId}
                )
                return SubscriptionResponse(
                    success=False,
                    message=error.message,
                    userFund=None,
                    error=error
                )
            
            # 2. Verificar que el fondo existe
            fund = await fund_service.get_fund_by_id(request.fundId)
            if not fund:
                error = SubscriptionError.from_code(
                    SubscriptionErrorCode.FUND_NOT_FOUND,
                    f"Fondo {request.fundId} no encontrado",
                    {"fundId": request.fundId}
                )
                return SubscriptionResponse(
                    success=False,
                    message=error.message,
                    userFund=None,
                    error=error
                )
            
            # 3. Verificar que el usuario no esté ya suscrito
            existing_subscription = await self.get_user_fund(request.userId, request.fundId)
            if existing_subscription:
                error = SubscriptionError.from_code(
                    SubscriptionErrorCode.ALREADY_SUBSCRIBED,
                    f"El usuario ya está suscrito al fondo {request.fundId}",
                    {"userId": request.userId, "fundId": request.fundId}
                )
                return SubscriptionResponse(
                    success=False,
                    message=error.message,
                    userFund=None,
                    error=error
                )
            
            # 4. Verificar saldo suficiente
            if user.balance < fund.minAmount:
                error = SubscriptionError.from_code(
                    SubscriptionErrorCode.INSUFFICIENT_BALANCE,
                    f"Saldo insuficiente. Se requiere un mínimo de {fund.minAmount}, saldo actual: {user.balance}",
                    {
                        "requiredAmount": float(fund.minAmount),
                        "currentBalance": float(user.balance),
                        "userId": request.userId,
                        "fundId": request.fundId
                    }
                )
                return SubscriptionResponse(
                    success=False,
                    message=error.message,
                    userFund=None,
                    error=error
                )
            
            # 5. Crear la suscripción
            subscription_time = datetime.now()
            user_fund = UserFund(
                userId=request.userId,
                fundId=request.fundId,
                subscribedAt=subscription_time
            )
            
            # Guardar en DynamoDB
            item = {
                'userId': user_fund.userId,
                'fundId': user_fund.fundId,
                'subscribedAt': user_fund.subscribedAt.isoformat()
            }
            self.table.put_item(Item=item)
            
            # 6. Debitar el monto mínimo del usuario
            new_balance = user.balance - fund.minAmount
            await user_service.update_user_balance(request.userId, new_balance)
            
            # 7. Registrar la transacción
            transaction_data = TransactionCreate(
                userId=request.userId,
                fundId=request.fundId,
                type="subscribe",
                amount=fund.minAmount
            )
            await transaction_service.create_transaction(transaction_data)
            
            # 8. Enviar notificación
            notification_sent = notification_service.send_subscription_notification(
                user.notificationType,
                request.userId,  # En un sistema real, sería email/teléfono
                fund.name
            )
            
            message = f"Suscripción exitosa al fondo {fund.name}. Monto debitado: {fund.minAmount}"
            if notification_sent:
                message += f". Notificación enviada vía {user.notificationType}."
            
            logger.info(f"User {request.userId} successfully subscribed to fund {request.fundId}")
            
            return SubscriptionResponse(
                success=True,
                message=message,
                userFund=user_fund
            )
            
        except Exception as e:
            logger.error(f"Error subscribing user {request.userId} to fund {request.fundId}: {str(e)}")
            error = SubscriptionError.from_code(
                SubscriptionErrorCode.INTERNAL_ERROR,
                f"Error interno: {str(e)}",
                {"userId": request.userId, "fundId": request.fundId, "exception": str(e)}
            )
            return SubscriptionResponse(
                success=False,
                message=error.message,
                userFund=None,
                error=error
            )
    
    async def unsubscribe_from_fund(self, request: UnsubscribeRequest) -> SubscriptionResponse:
        """
        Cancelar suscripción de un usuario a un fondo
        
        Reglas de negocio:
        1. El usuario debe existir
        2. El fondo debe existir
        3. El usuario debe estar suscrito al fondo
        4. Se debe eliminar la suscripción
        5. Se debe registrar la transacción de cancelación
        6. Se debe enviar notificación según preferencia del usuario
        """
        try:
            # 1. Verificar que el usuario existe
            user = await user_service.get_user_by_id(request.userId)
            if not user:
                error = SubscriptionError.from_code(
                    SubscriptionErrorCode.USER_NOT_FOUND,
                    f"Usuario {request.userId} no encontrado",
                    {"userId": request.userId}
                )
                return SubscriptionResponse(
                    success=False,
                    message=error.message,
                    userFund=None,
                    error=error
                )
            
            # 2. Verificar que el fondo existe
            fund = await fund_service.get_fund_by_id(request.fundId)
            if not fund:
                error = SubscriptionError.from_code(
                    SubscriptionErrorCode.FUND_NOT_FOUND,
                    f"Fondo {request.fundId} no encontrado",
                    {"fundId": request.fundId}
                )
                return SubscriptionResponse(
                    success=False,
                    message=error.message,
                    userFund=None,
                    error=error
                )
            
            # 3. Verificar que el usuario esté suscrito
            existing_subscription = await self.get_user_fund(request.userId, request.fundId)
            if not existing_subscription:
                error = SubscriptionError.from_code(
                    SubscriptionErrorCode.NOT_SUBSCRIBED,
                    f"El usuario no está suscrito al fondo {request.fundId}",
                    {"userId": request.userId, "fundId": request.fundId}
                )
                return SubscriptionResponse(
                    success=False,
                    message=error.message,
                    userFund=None,
                    error=error
                )
            
            # 4. Eliminar la suscripción
            self.table.delete_item(
                Key={
                    'userId': request.userId,
                    'fundId': request.fundId
                }
            )
            
            # 5. Registrar la transacción de cancelación (monto 0)
            transaction_data = TransactionCreate(
                userId=request.userId,
                fundId=request.fundId,
                type="unsubscribe",
                amount=Decimal("0")
            )
            await transaction_service.create_transaction(transaction_data)
            
            # 6. Enviar notificación
            notification_sent = notification_service.send_unsubscription_notification(
                user.notificationType,
                request.userId,  # En un sistema real, sería email/teléfono
                fund.name
            )
            
            message = f"Cancelación exitosa de la suscripción al fondo {fund.name}"
            if notification_sent:
                message += f". Notificación enviada vía {user.notificationType}."
            
            logger.info(f"User {request.userId} successfully unsubscribed from fund {request.fundId}")
            
            return SubscriptionResponse(
                success=True,
                message=message,
                userFund=None
            )
            
        except Exception as e:
            logger.error(f"Error unsubscribing user {request.userId} from fund {request.fundId}: {str(e)}")
            error = SubscriptionError.from_code(
                SubscriptionErrorCode.INTERNAL_ERROR,
                f"Error interno: {str(e)}",
                {"userId": request.userId, "fundId": request.fundId, "exception": str(e)}
            )
            return SubscriptionResponse(
                success=False,
                message=error.message,
                userFund=None,
                error=error
            )
    
    async def get_user_fund(self, user_id: str, fund_id: str) -> Optional[UserFund]:
        """Obtener una suscripción específica usuario-fondo"""
        try:
            response = self.table.get_item(
                Key={
                    'userId': user_id,
                    'fundId': fund_id
                }
            )
            
            if 'Item' not in response:
                return None
            
            item = response['Item']
            user_fund = UserFund(
                userId=item['userId'],
                fundId=item['fundId'],
                subscribedAt=datetime.fromisoformat(item['subscribedAt'])
            )
            
            return user_fund
            
        except ClientError as e:
            logger.error(f"Error retrieving subscription for user {user_id} and fund {fund_id}: {str(e)}")
            return None
    
    async def get_user_subscriptions(self, user_id: str) -> List[UserFund]:
        """Obtener todas las suscripciones de un usuario"""
        try:
            response = self.table.query(
                KeyConditionExpression='userId = :userId',
                ExpressionAttributeValues={':userId': user_id}
            )
            
            subscriptions_data = response.get('Items', [])
            
            subscriptions = []
            for item in subscriptions_data:
                user_fund = UserFund(
                    userId=item['userId'],
                    fundId=item['fundId'],
                    subscribedAt=datetime.fromisoformat(item['subscribedAt'])
                )
                subscriptions.append(user_fund)
            
            # Ordenar por fecha de suscripción (más recientes primero)
            subscriptions.sort(key=lambda x: x.subscribedAt, reverse=True)
            
            logger.info(f"Retrieved {len(subscriptions)} subscriptions for user {user_id}")
            return subscriptions
            
        except ClientError as e:
            logger.error(f"Error retrieving subscriptions for user {user_id}: {str(e)}")
            raise Exception(f"Error al obtener suscripciones del usuario {user_id}: {str(e)}")

# Instancia global del servicio
subscription_service = SubscriptionService() 