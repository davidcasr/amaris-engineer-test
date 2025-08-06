import boto3
from botocore.exceptions import ClientError
from app.config import DYNAMODB_ENDPOINT, AWS_REGION
import logging

logger = logging.getLogger(__name__)

class DynamoDBClient:
    """Cliente para conectarse a DynamoDB Local"""
    
    def __init__(self):
        self.dynamodb = None
        self.dynamodb_resource = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Inicializar cliente y resource de DynamoDB"""
        try:
            # Cliente para operaciones administrativas
            self.dynamodb = boto3.client(
                'dynamodb',
                endpoint_url=DYNAMODB_ENDPOINT,
                region_name=AWS_REGION,
                aws_access_key_id='dummy',
                aws_secret_access_key='dummy'
            )
            
            # Resource para operaciones de datos
            self.dynamodb_resource = boto3.resource(
                'dynamodb',
                endpoint_url=DYNAMODB_ENDPOINT,
                region_name=AWS_REGION,
                aws_access_key_id='dummy',
                aws_secret_access_key='dummy'
            )
            
            logger.info(f"DynamoDB client initialized successfully. Endpoint: {DYNAMODB_ENDPOINT}")
            
        except Exception as e:
            logger.error(f"Error initializing DynamoDB client: {str(e)}")
            raise
    
    def get_client(self):
        """Obtener cliente DynamoDB"""
        return self.dynamodb
    
    def get_resource(self):
        """Obtener resource DynamoDB"""
        return self.dynamodb_resource
    
    def get_table(self, table_name: str):
        """Obtener referencia a una tabla específica"""
        try:
            return self.dynamodb_resource.Table(table_name)
        except Exception as e:
            logger.error(f"Error getting table {table_name}: {str(e)}")
            raise
    
    def health_check(self) -> bool:
        """Verificar conectividad con DynamoDB"""
        try:
            self.dynamodb.list_tables()
            return True
        except ClientError as e:
            logger.error(f"DynamoDB health check failed: {str(e)}")
            return False

# Instancia global del cliente
db_client = DynamoDBClient() 