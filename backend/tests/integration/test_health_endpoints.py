"""
Tests de integración para endpoints de health check
"""
import pytest
from unittest.mock import patch, Mock
from fastapi.testclient import TestClient
from app.main import app


class TestHealthEndpoints:
    """Tests para endpoints de health check"""
    
    @pytest.fixture
    def client(self):
        """Cliente de testing para FastAPI"""
        return TestClient(app)
    
    def test_health_check_success(self, client):
        """Test health check cuando DynamoDB está disponible"""
        # Arrange
        mock_response = {'TableNames': ['Users', 'Funds', 'UserFunds', 'Transactions']}
        
        # Act
        with patch('boto3.client') as mock_boto3:
            mock_dynamodb_client = Mock()
            mock_dynamodb_client.list_tables.return_value = mock_response
            mock_boto3.return_value = mock_dynamodb_client
            
            response = client.get("/api/v1/health")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        
        assert data["status"] == "healthy"
        assert data["service"] == "Plataforma de Fondos API"
        assert data["version"] == "1.0.0"
        assert data["database"]["status"] == "connected"
        assert data["database"]["tables_count"] == 4
        assert "timestamp" in data
    
    def test_health_check_database_error(self, client):
        """Test health check cuando DynamoDB no está disponible"""
        # Arrange & Act
        with patch('boto3.client') as mock_boto3:
            mock_dynamodb_client = Mock()
            mock_dynamodb_client.list_tables.side_effect = Exception("Connection refused")
            mock_boto3.return_value = mock_dynamodb_client
            
            response = client.get("/api/v1/health")
        
        # Assert
        assert response.status_code == 200  # Endpoint siempre retorna 200
        data = response.json()
        
        assert data["status"] == "unhealthy"
        assert data["service"] == "Plataforma de Fondos API"
        assert data["version"] == "1.0.0"
        assert data["database"]["status"] == "disconnected"
        assert "error" in data["database"]
        assert "Connection refused" in data["database"]["error"]
        assert "timestamp" in data
    
    def test_health_check_response_structure(self, client):
        """Test estructura completa de la respuesta del health check"""
        # Act
        with patch('boto3.client') as mock_boto3:
            mock_dynamodb_client = Mock()
            mock_dynamodb_client.list_tables.return_value = {'TableNames': []}
            mock_boto3.return_value = mock_dynamodb_client
            
            response = client.get("/api/v1/health")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        
        # Verificar estructura requerida
        required_fields = ["status", "timestamp", "service", "version", "database"]
        for field in required_fields:
            assert field in data
        
        # Verificar estructura de database
        database_fields = ["status", "endpoint", "region"]
        for field in database_fields:
            assert field in data["database"]
    
    def test_health_check_timestamps_are_iso_format(self, client):
        """Test que los timestamps están en formato ISO"""
        # Act
        with patch('boto3.client') as mock_boto3:
            mock_dynamodb_client = Mock()
            mock_dynamodb_client.list_tables.return_value = {'TableNames': []}
            mock_boto3.return_value = mock_dynamodb_client
            
            response = client.get("/api/v1/health")
        
        # Assert
        data = response.json()
        timestamp = data["timestamp"]
        
        # Verificar que el timestamp es un string válido en formato ISO
        from datetime import datetime
        try:
            datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        except ValueError:
            pytest.fail(f"Timestamp '{timestamp}' is not in valid ISO format")