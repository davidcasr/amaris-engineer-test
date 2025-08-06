import logging
from typing import Literal

logger = logging.getLogger(__name__)

class NotificationService:
    """Servicio para envío de notificaciones"""
    
    def send_notification(self, notification_type: Literal["email", "sms"], recipient: str, message: str) -> bool:
        """
        Enviar notificación según el tipo especificado
        
        Args:
            notification_type: Tipo de notificación ("email" o "sms")
            recipient: Destinatario de la notificación
            message: Mensaje a enviar
            
        Returns:
            bool: True si se envió exitosamente, False en caso contrario
            
        Raises:
            ValueError: Si el tipo de notificación no es soportado
        """
        try:
            if notification_type == "email":
                self._send_email(recipient, message)
                logger.info(f"[Email] Notification sent to {recipient}")
                return True
            elif notification_type == "sms":
                self._send_sms(recipient, message)
                logger.info(f"[SMS] Notification sent to {recipient}")
                return True
            else:
                raise ValueError(f"Unsupported notification type: {notification_type}")
                
        except Exception as e:
            logger.error(f"Error sending {notification_type} notification to {recipient}: {str(e)}")
            return False
    
    def _send_email(self, recipient: str, message: str) -> None:
        """
        Simulación de envío de email
        En producción, aquí se integraría con AWS SES o similar
        """
        print(f"[Email] Sending to {recipient}: {message}")
        # TODO: Integrar con AWS SES en producción
        logger.debug(f"Email notification simulated for {recipient}")
    
    def _send_sms(self, recipient: str, message: str) -> None:
        """
        Simulación de envío de SMS
        En producción, aquí se integraría con AWS SNS o similar
        """
        print(f"[SMS] Sending to {recipient}: {message}")
        # TODO: Integrar con AWS SNS en producción
        logger.debug(f"SMS notification simulated for {recipient}")
    
    def send_subscription_notification(self, notification_type: str, recipient: str, fund_name: str) -> bool:
        """Enviar notificación específica de suscripción exitosa"""
        message = f"Te has suscrito exitosamente al fondo {fund_name}. ¡Gracias por confiar en nosotros!"
        return self.send_notification(notification_type, recipient, message)
    
    def send_unsubscription_notification(self, notification_type: str, recipient: str, fund_name: str) -> bool:
        """Enviar notificación específica de cancelación de suscripción"""
        message = f"Has cancelado tu suscripción al fondo {fund_name}. Esperamos verte pronto de nuevo."
        return self.send_notification(notification_type, recipient, message)

# Instancia global del servicio
notification_service = NotificationService() 