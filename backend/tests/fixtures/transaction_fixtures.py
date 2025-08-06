"""
Fixtures para datos de transacciones de prueba
"""
import pytest
from datetime import datetime
from decimal import Decimal
from app.models.transaction import Transaction, TransactionCreate


@pytest.fixture
def sample_transaction():
    """Transacción de prueba básica"""
    return Transaction(
        transactionId="txn_123456789",
        userId="user123",
        fundId="FPV_BTG_PACTUAL",
        type="subscribe",
        amount=Decimal("75000"),
        timestamp=datetime(2024, 1, 15, 10, 30, 0)
    )


@pytest.fixture
def sample_unsubscribe_transaction():
    """Transacción de cancelación de prueba"""
    return Transaction(
        transactionId="txn_987654321",
        userId="user123",
        fundId="FPV_BTG_PACTUAL",
        type="unsubscribe",
        amount=Decimal("75000"),
        timestamp=datetime(2024, 1, 20, 15, 45, 0)
    )


@pytest.fixture
def sample_transaction_create():
    """Datos para crear una transacción"""
    return TransactionCreate(
        userId="user123",
        fundId="FPV_BTG_PACTUAL",
        type="subscribe",
        amount=Decimal("75000")
    )


@pytest.fixture
def transaction_data_dict():
    """Datos de transacción en formato dict (como viene de DynamoDB)"""
    return {
        'transactionId': 'txn_123456789',
        'userId': 'user123',
        'fundId': 'FPV_BTG_PACTUAL',
        'type': 'subscribe',
        'amount': Decimal('75000'),
        'timestamp': '2024-01-15T10:30:00'
    }


@pytest.fixture
def sample_transactions_list(sample_transaction, sample_unsubscribe_transaction):
    """Lista de transacciones de prueba"""
    return [sample_transaction, sample_unsubscribe_transaction]