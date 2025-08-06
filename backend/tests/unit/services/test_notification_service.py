"""
Tests unitarios para NotificationService
"""
import pytest
from unittest.mock import Mock, patch

from app.services.notification_service import notification_service


class TestNotificationService:
    """Tests para NotificationService"""
    
    def test_send_email_notification(self):
        """Test envío de notificación por email"""
        # Arrange
        recipient = "test@example.com"
        message = "Test message"
        
        # Act
        with patch('builtins.print') as mock_print:
            result = notification_service.send_notification("email", recipient, message)
        
        # Assert
        assert result is True
        mock_print.assert_called_once_with(f"[Email] Sending to {recipient}: {message}")
    
    def test_send_sms_notification(self):
        """Test envío de notificación por SMS"""
        # Arrange
        recipient = "+573001234567"
        message = "Test SMS message"
        
        # Act
        with patch('builtins.print') as mock_print:
            result = notification_service.send_notification("sms", recipient, message)
        
        # Assert
        assert result is True
        mock_print.assert_called_once_with(f"[SMS] Sending to {recipient}: {message}")
    

    
    def test_send_subscription_notification_email(self):
        """Test notificación de suscripción por email"""
        # Arrange
        fund_name = "FPV_BTG_PACTUAL"
        recipient = "juan@example.com"
        notification_type = "email"
        
        # Act
        with patch('builtins.print') as mock_print:
            result = notification_service.send_subscription_notification(
                notification_type, recipient, fund_name
            )
        
        # Assert
        assert result is True
        expected_message = f"Te has suscrito exitosamente al fondo {fund_name}. ¡Gracias por confiar en nosotros!"
        mock_print.assert_called_once_with(f"[Email] Sending to {recipient}: {expected_message}")
    
    def test_send_subscription_notification_sms(self):
        """Test notificación de suscripción por SMS"""
        # Arrange
        fund_name = "DEUDAPRIVADA"
        recipient = "+573009876543"
        notification_type = "sms"
        
        # Act
        with patch('builtins.print') as mock_print:
            result = notification_service.send_subscription_notification(
                notification_type, recipient, fund_name
            )
        
        # Assert
        assert result is True
        expected_message = f"Te has suscrito exitosamente al fondo {fund_name}. ¡Gracias por confiar en nosotros!"
        mock_print.assert_called_once_with(f"[SMS] Sending to {recipient}: {expected_message}")
    
    def test_send_unsubscription_notification(self):
        """Test notificación de cancelación de suscripción"""
        # Arrange
        fund_name = "FDO-ACCIONES"
        recipient = "carlos@example.com"
        notification_type = "email"
        
        # Act
        with patch('builtins.print') as mock_print:
            result = notification_service.send_unsubscription_notification(
                notification_type, recipient, fund_name
            )
        
        # Assert
        assert result is True
        expected_message = f"Has cancelado tu suscripción al fondo {fund_name}. Esperamos verte pronto de nuevo."
        mock_print.assert_called_once_with(f"[Email] Sending to {recipient}: {expected_message}")