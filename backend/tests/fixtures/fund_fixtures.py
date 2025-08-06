"""
Fixtures para datos de fondos de prueba
"""
import pytest
from decimal import Decimal
from app.models.fund import Fund


@pytest.fixture
def sample_fund():
    """Fondo de prueba básico"""
    return Fund(
        fundId="FPV_BTG_PACTUAL",
        name="FPV_BTG_PACTUAL",
        category="FPV",
        minAmount=Decimal("75000")
    )


@pytest.fixture
def sample_fund_2():
    """Segundo fondo de prueba"""
    return Fund(
        fundId="DEUDAPRIVADA",
        name="DEUDAPRIVADA",
        category="FIC",
        minAmount=Decimal("50000")
    )


@pytest.fixture
def sample_fund_3():
    """Tercer fondo de prueba con monto mínimo bajo"""
    return Fund(
        fundId="FDO-ACCIONES",
        name="FDO-ACCIONES",
        category="FIC",
        minAmount=Decimal("25000")
    )


@pytest.fixture
def sample_funds_list(sample_fund, sample_fund_2, sample_fund_3):
    """Lista de fondos de prueba"""
    return [sample_fund, sample_fund_2, sample_fund_3]


@pytest.fixture
def fund_data_dict():
    """Datos de fondo en formato dict (como viene de DynamoDB)"""
    return {
        'fundId': 'FPV_BTG_PACTUAL',
        'name': 'FPV_BTG_PACTUAL',
        'category': 'FPV',
        'minAmount': Decimal('75000')
    }