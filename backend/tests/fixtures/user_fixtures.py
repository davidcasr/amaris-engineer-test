"""
Fixtures para datos de usuarios de prueba
"""
import pytest
from decimal import Decimal
from app.models.user import User


@pytest.fixture
def sample_user():
    """Usuario de prueba básico con saldo suficiente"""
    return User(
        userId="user123",
        balance=Decimal("500000"),
        notificationType="email"
    )


@pytest.fixture
def sample_user_sms():
    """Usuario de prueba que prefiere notificaciones por SMS"""
    return User(
        userId="user456",
        balance=Decimal("100000"),
        notificationType="sms"
    )


@pytest.fixture
def sample_user_low_balance():
    """Usuario de prueba con saldo insuficiente"""
    return User(
        userId="user789",
        balance=Decimal("10000"),
        notificationType="email"
    )


@pytest.fixture
def user_data_dict():
    """Datos de usuario en formato dict (como viene de DynamoDB)"""
    return {
        'userId': 'user123',
        'balance': Decimal('500000'),
        'notificationType': 'email'
    }