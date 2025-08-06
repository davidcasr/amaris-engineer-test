"""
Configuración global de pytest y fixtures compartidas
"""
import pytest
import os
from typing import Generator
from unittest.mock import Mock, patch
from fastapi.testclient import TestClient
from moto import mock_aws
import boto3
from decimal import Decimal

# Configurar variables de entorno para testing
os.environ["ENVIRONMENT"] = "test"
os.environ["DYNAMODB_ENDPOINT"] = "http://localhost:8000"
os.environ["AWS_REGION"] = "us-east-1"
os.environ["AWS_ACCESS_KEY_ID"] = "testing"
os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"

@pytest.fixture(scope="session")
def dynamodb_mock():
    """Mock de DynamoDB para toda la sesión de testing"""
    with mock_aws():
        yield


@pytest.fixture
def dynamodb_client(dynamodb_mock):
    """Cliente de DynamoDB mockeado para tests"""
    client = boto3.client(
        'dynamodb',
        region_name='us-east-1',
        aws_access_key_id='testing',
        aws_secret_access_key='testing'
    )
    
    # Crear tablas necesarias para tests
    create_test_tables(client)
    return client


@pytest.fixture
def dynamodb_resource(dynamodb_mock):
    """Recurso de DynamoDB mockeado para tests"""
    resource = boto3.resource(
        'dynamodb',
        region_name='us-east-1',
        aws_access_key_id='testing',
        aws_secret_access_key='testing'
    )
    return resource


def create_test_tables(dynamodb_client):
    """Crear todas las tablas necesarias para testing"""
    
    # Tabla Users
    try:
        dynamodb_client.create_table(
            TableName='Users',
            KeySchema=[
                {'AttributeName': 'userId', 'KeyType': 'HASH'}
            ],
            AttributeDefinitions=[
                {'AttributeName': 'userId', 'AttributeType': 'S'}
            ],
            BillingMode='PAY_PER_REQUEST'
        )
    except:
        pass
    
    # Tabla Funds
    try:
        dynamodb_client.create_table(
            TableName='Funds',
            KeySchema=[
                {'AttributeName': 'fundId', 'KeyType': 'HASH'}
            ],
            AttributeDefinitions=[
                {'AttributeName': 'fundId', 'AttributeType': 'S'}
            ],
            BillingMode='PAY_PER_REQUEST'
        )
    except:
        pass
    
    # Tabla UserFunds
    try:
        dynamodb_client.create_table(
            TableName='UserFunds',
            KeySchema=[
                {'AttributeName': 'userId', 'KeyType': 'HASH'},
                {'AttributeName': 'fundId', 'KeyType': 'RANGE'}
            ],
            AttributeDefinitions=[
                {'AttributeName': 'userId', 'AttributeType': 'S'},
                {'AttributeName': 'fundId', 'AttributeType': 'S'}
            ],
            BillingMode='PAY_PER_REQUEST'
        )
    except:
        pass
    
    # Tabla Transactions
    try:
        dynamodb_client.create_table(
            TableName='Transactions',
            KeySchema=[
                {'AttributeName': 'transactionId', 'KeyType': 'HASH'}
            ],
            AttributeDefinitions=[
                {'AttributeName': 'transactionId', 'AttributeType': 'S'},
                {'AttributeName': 'userId', 'AttributeType': 'S'}
            ],
            GlobalSecondaryIndexes=[
                {
                    'IndexName': 'UserIdIndex',
                    'KeySchema': [
                        {'AttributeName': 'userId', 'KeyType': 'HASH'}
                    ],
                    'Projection': {'ProjectionType': 'ALL'}
                }
            ],
            BillingMode='PAY_PER_REQUEST'
        )
    except:
        pass


@pytest.fixture
def test_client() -> Generator[TestClient, None, None]:
    """Cliente de testing para FastAPI"""
    from app.main import app
    with TestClient(app) as client:
        yield client


@pytest.fixture
def mock_notification_service():
    """Mock del servicio de notificaciones"""
    with patch('app.services.notification_service.notification_service') as mock:
        mock.send_notification = Mock()
        yield mock