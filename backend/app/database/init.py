from botocore.exceptions import ClientError
from app.database.client import db_client
from app.config import INITIAL_AMOUNT
import logging
from decimal import Decimal

logger = logging.getLogger(__name__)

def create_tables():
    """Crear todas las tablas necesarias para la aplicación"""
    tables_config = [
        {
            "TableName": "Funds",
            "KeySchema": [
                {"AttributeName": "fundId", "KeyType": "HASH"}
            ],
            "AttributeDefinitions": [
                {"AttributeName": "fundId", "AttributeType": "S"}
            ],
            "ProvisionedThroughput": {
                "ReadCapacityUnits": 5,
                "WriteCapacityUnits": 5
            }
        },
        {
            "TableName": "User",
            "KeySchema": [
                {"AttributeName": "userId", "KeyType": "HASH"}
            ],
            "AttributeDefinitions": [
                {"AttributeName": "userId", "AttributeType": "S"}
            ],
            "ProvisionedThroughput": {
                "ReadCapacityUnits": 5,
                "WriteCapacityUnits": 5
            }
        },
        {
            "TableName": "UserFunds",
            "KeySchema": [
                {"AttributeName": "userId", "KeyType": "HASH"},
                {"AttributeName": "fundId", "KeyType": "RANGE"}
            ],
            "AttributeDefinitions": [
                {"AttributeName": "userId", "AttributeType": "S"},
                {"AttributeName": "fundId", "AttributeType": "S"}
            ],
            "ProvisionedThroughput": {
                "ReadCapacityUnits": 5,
                "WriteCapacityUnits": 5
            }
        },
        {
            "TableName": "Transactions",
            "KeySchema": [
                {"AttributeName": "transactionId", "KeyType": "HASH"}
            ],
            "AttributeDefinitions": [
                {"AttributeName": "transactionId", "AttributeType": "S"},
                {"AttributeName": "userId", "AttributeType": "S"}
            ],
            "GlobalSecondaryIndexes": [
                {
                    "IndexName": "UserIdIndex",
                    "KeySchema": [
                        {"AttributeName": "userId", "KeyType": "HASH"}
                    ],
                    "Projection": {"ProjectionType": "ALL"},
                    "ProvisionedThroughput": {
                        "ReadCapacityUnits": 5,
                        "WriteCapacityUnits": 5
                    }
                }
            ],
            "ProvisionedThroughput": {
                "ReadCapacityUnits": 5,
                "WriteCapacityUnits": 5
            }
        }
    ]
    
    dynamodb = db_client.get_client()
    
    for table_config in tables_config:
        table_name = table_config["TableName"]
        try:
            # Verificar si la tabla ya existe
            existing_tables = dynamodb.list_tables()["TableNames"]
            
            if table_name not in existing_tables:
                logger.info(f"Creating table {table_name}...")
                dynamodb.create_table(**table_config)
                
                # Esperar a que la tabla esté activa
                waiter = dynamodb.get_waiter('table_exists')
                waiter.wait(TableName=table_name, WaiterConfig={'Delay': 1, 'MaxAttempts': 30})
                
                logger.info(f"Table {table_name} created successfully")
            else:
                logger.info(f"Table {table_name} already exists")
                
        except ClientError as e:
            logger.error(f"Error creating table {table_name}: {str(e)}")
            raise

def populate_initial_data():
    """Poblar las tablas con datos iniciales para testing"""
    
    # Datos iniciales de fondos
    funds_data = [
        {
            "fundId": "FPV_BTG_PACTUAL",
            "name": "FPV_BTG_PACTUAL", 
            "category": "FPV",
            "minAmount": Decimal("75000")
        },
        {
            "fundId": "FPV_RECAUDADORA",
            "name": "FPV_RECAUDADORA",
            "category": "FPV", 
            "minAmount": Decimal("125000")
        },
        {
            "fundId": "FIC_MANDATO",
            "name": "FIC_MANDATO",
            "category": "FIC",
            "minAmount": Decimal("500000")
        },
        {
            "fundId": "FPV_DEUDAPRIVADA",
            "name": "FPV_DEUDAPRIVADA",
            "category": "FPV",
            "minAmount": Decimal("50000")
        },
        {
            "fundId": "FIC_ACCIONES",
            "name": "FIC_ACCIONES", 
            "category": "FIC",
            "minAmount": Decimal("250000")
        }
    ]
    
    # Usuario de prueba
    test_user = {
        "userId": "user123",
        "balance": INITIAL_AMOUNT,
        "notificationType": "email"
    }
    
    try:
        # Poblar tabla Funds
        funds_table = db_client.get_table("Funds")
        for fund in funds_data:
            try:
                funds_table.put_item(Item=fund)
                logger.info(f"Added fund: {fund['fundId']}")
            except ClientError as e:
                if e.response['Error']['Code'] != 'ConditionalCheckFailedException':
                    logger.error(f"Error adding fund {fund['fundId']}: {str(e)}")
        
        # Poblar usuario de prueba
        user_table = db_client.get_table("User")
        try:
            user_table.put_item(Item=test_user)
            logger.info(f"Added test user: {test_user['userId']}")
        except ClientError as e:
            if e.response['Error']['Code'] != 'ConditionalCheckFailedException':
                logger.error(f"Error adding test user: {str(e)}")
                
        logger.info("Initial data population completed")
        
    except Exception as e:
        logger.error(f"Error populating initial data: {str(e)}")
        raise

def initialize_database():
    """Función principal para inicializar la base de datos completa"""
    logger.info("Starting database initialization...")
    
    try:
        # Crear tablas
        create_tables()
        
        # Poblar datos iniciales
        populate_initial_data()
        
        logger.info("Database initialization completed successfully")
        
    except Exception as e:
        logger.error(f"Database initialization failed: {str(e)}")
        raise

if __name__ == "__main__":
    # Configurar logging
    logging.basicConfig(level=logging.INFO)
    initialize_database() 