"""
Tests unitarios para los modelos Pydantic
"""
import pytest
from decimal import Decimal
from datetime import datetime
from pydantic import ValidationError

from app.models.fund import Fund
from app.models.user import User
from app.models.transaction import Transaction, TransactionCreate
from app.models.subscription import (
    SubscribeRequest, UnsubscribeRequest, UserFund, 
    SubscriptionResponse, SubscriptionError
)
from app.models.settings import NotificationSettingsRequest


class TestFundModel:
    """Tests para el modelo Fund"""
    
    def test_fund_creation_valid(self):
        """Test creación válida de fondo"""
        fund = Fund(
            fundId="TEST_FUND",
            name="Test Fund",
            category="FPV",
            minAmount=Decimal("50000")
        )
        
        assert fund.fundId == "TEST_FUND"
        assert fund.name == "Test Fund"
        assert fund.category == "FPV"
        assert fund.minAmount == Decimal("50000")
    
    def test_fund_invalid_min_amount(self):
        """Test validación de monto mínimo negativo"""
        with pytest.raises(ValidationError):
            Fund(
                fundId="TEST_FUND",
                name="Test Fund",
                category="FPV",
                minAmount=Decimal("-1000")
            )
    



class TestUserModel:
    """Tests para el modelo User"""
    
    def test_user_creation_valid(self):
        """Test creación válida de usuario"""
        user = User(
            userId="test_user",
            balance=Decimal("100000"),
            notificationType="email"
        )
        
        assert user.userId == "test_user"
        assert user.balance == Decimal("100000")
        assert user.notificationType == "email"
    
    def test_user_invalid_notification_type(self):
        """Test validación de tipo de notificación inválido"""
        with pytest.raises(ValidationError):
            User(
                userId="test_user",
                balance=Decimal("100000"),
                notificationType="invalid_type"
            )
    
    def test_user_negative_balance(self):
        """Test validación de balance negativo"""
        with pytest.raises(ValidationError):
            User(
                userId="test_user",
                balance=Decimal("-1000"),
                notificationType="email"
            )


class TestTransactionModel:
    """Tests para el modelo Transaction"""
    
    def test_transaction_creation_valid(self):
        """Test creación válida de transacción"""
        transaction = Transaction(
            userId="user_123",
            fundId="fund_123",
            type="subscribe",
            amount=Decimal("50000")
        )
        
        assert transaction.userId == "user_123"
        assert transaction.type == "subscribe"
        assert transaction.amount == Decimal("50000")
    
    def test_transaction_invalid_type(self):
        """Test validación de tipo de transacción inválido"""
        with pytest.raises(ValidationError):
            Transaction(
                userId="user_123",
                fundId="fund_123",
                type="INVALID_TYPE",
                amount=Decimal("50000")
            )
    
    def test_transaction_create_model(self):
        """Test modelo TransactionCreate"""
        transaction_create = TransactionCreate(
            userId="user_123",
            fundId="fund_123",
            type="subscribe",
            amount=Decimal("50000")
        )
        
        assert transaction_create.userId == "user_123"
        assert transaction_create.type == "subscribe"


class TestSubscriptionModels:
    """Tests para los modelos de suscripción"""
    
    def test_subscribe_request_valid(self):
        """Test creación válida de SubscribeRequest"""
        request = SubscribeRequest(
            userId="user_123",
            fundId="fund_123"
        )
        
        assert request.userId == "user_123"
        assert request.fundId == "fund_123"
    
    def test_user_fund_creation(self):
        """Test creación de UserFund"""
        user_fund = UserFund(
            userId="user_123",
            fundId="fund_123",
            subscribedAt=datetime.now()
        )
        
        assert user_fund.userId == "user_123"
        assert user_fund.fundId == "fund_123"
        assert isinstance(user_fund.subscribedAt, datetime)
    

    
    def test_subscription_response_error(self):
        """Test SubscriptionResponse con error"""
        error = SubscriptionError(
            code="USER_NOT_FOUND",
            message="Usuario no encontrado",
            status_code=404,
            details={"userId": "invalid_user"}
        )
        
        response = SubscriptionResponse(
            success=False,
            message="Error en suscripción",
            userFund=None,
            error=error
        )
        
        assert response.success is False
        assert response.userFund is None
        assert response.error is not None
        assert response.error.code == "USER_NOT_FOUND"


class TestSettingsModels:
    """Tests para los modelos de configuración"""
    
    def test_notification_settings_request_valid(self):
        """Test NotificationSettingsRequest válido"""
        request = NotificationSettingsRequest(
            userId="user_123",
            notificationType="sms"
        )
        
        assert request.userId == "user_123"
        assert request.notificationType == "sms"
    
    def test_notification_settings_invalid_type(self):
        """Test tipo de notificación inválido"""
        with pytest.raises(ValidationError):
            NotificationSettingsRequest(
                userId="user_123",
                notificationType="invalid_type"
            )