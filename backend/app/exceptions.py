"""
Excepciones personalizadas para la aplicación de fondos
"""

class FundNotFoundException(Exception):
    """Excepción cuando un fondo no es encontrado"""
    def __init__(self, fund_id: str):
        self.fund_id = fund_id
        super().__init__(f"Fondo {fund_id} no encontrado")

class UserNotFoundException(Exception):
    """Excepción cuando un usuario no es encontrado"""
    def __init__(self, user_id: str):
        self.user_id = user_id
        super().__init__(f"Usuario {user_id} no encontrado")

class InsufficientBalanceException(Exception):
    """Excepción cuando el usuario no tiene saldo suficiente"""
    def __init__(self, required_amount: float, current_balance: float):
        self.required_amount = required_amount
        self.current_balance = current_balance
        super().__init__(
            f"Saldo insuficiente. Se requiere {required_amount}, saldo actual: {current_balance}"
        )

class AlreadySubscribedException(Exception):
    """Excepción cuando el usuario ya está suscrito al fondo"""
    def __init__(self, user_id: str, fund_id: str):
        self.user_id = user_id
        self.fund_id = fund_id
        super().__init__(f"El usuario {user_id} ya está suscrito al fondo {fund_id}")

class NotSubscribedException(Exception):
    """Excepción cuando el usuario no está suscrito al fondo"""
    def __init__(self, user_id: str, fund_id: str):
        self.user_id = user_id
        self.fund_id = fund_id
        super().__init__(f"El usuario {user_id} no está suscrito al fondo {fund_id}")

class InvalidNotificationTypeException(Exception):
    """Excepción cuando el tipo de notificación es inválido"""
    def __init__(self, notification_type: str):
        self.notification_type = notification_type
        super().__init__(
            f"Tipo de notificación inválido: {notification_type}. Tipos válidos: email, sms"
        )

class TransactionNotFoundException(Exception):
    """Excepción cuando una transacción no es encontrada"""
    def __init__(self, transaction_id: str):
        self.transaction_id = transaction_id
        super().__init__(f"Transacción {transaction_id} no encontrada")

class DatabaseException(Exception):
    """Excepción general para errores de base de datos"""
    def __init__(self, message: str):
        super().__init__(f"Error de base de datos: {message}")

class ValidationException(Exception):
    """Excepción para errores de validación de datos"""
    def __init__(self, message: str):
        super().__init__(f"Error de validación: {message}")

class BusinessRuleException(Exception):
    """Excepción para violaciones de reglas de negocio"""
    def __init__(self, message: str):
        super().__init__(f"Regla de negocio violada: {message}") 