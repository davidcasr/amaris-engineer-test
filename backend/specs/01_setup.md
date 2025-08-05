Esta guía define los pasos necesarios para configurar la base del backend de la aplicación de Fondos, utilizando FastAPI, DynamoDB Local, Docker y Docker Compose. Esta etapa incluye únicamente la creación de la aplicación base y un endpoint de salud (/health).

Paso 1: Descripción general del backend
El backend es una API REST desarrollada con FastAPI, orientada a gestionar la lógica de negocio de una plataforma de fondos de inversión. Se conecta a una base de datos DynamoDB, la cual se ejecutará localmente para desarrollo. El backend está preparado para escalar y ser desplegado en AWS como función Lambda, con el soporte de infraestructura como código usando CloudFormation.

Paso 2: Estructura de carpetas
Se utilizará la siguiente estructura inicial:

```
backend/
├── app/
│   ├── main.py              # App principal de FastAPI
│   ├── routes/
│   │   └── health.py        # Ruta para verificar el estado del servicio
│   ├── services/            # Lógica de negocio
│   ├── models/              # Esquemas de entrada/salida (Pydantic)
│   ├── database/            # Configuración de DynamoDB
│   └── config.py            # Configuración del entorno y constantes
├── Dockerfile
├── requirements.txt
```

Paso 3: Configuración de dependencias
En el archivo requirements.txt, definimos las dependencias principales:

```
fastapi
uvicorn
boto3
pydantic
python-dotenv
black
pylint
pytest
```

Paso 4: Configuración base de la aplicación (config.py)

```
# app/config.py
import os

DYNAMODB_ENDPOINT = os.getenv("DYNAMODB_ENDPOINT", "http://dynamodb:8000")
AWS_REGION = os.getenv("AWS_REGION", "us-west-2")
```

Crea también un archivo .env en la raíz del backend:

```
DYNAMODB_ENDPOINT=http://dynamodb:8000
AWS_REGION=us-west-2
```

Paso 5: Creación de la app básica con FastAPI (main.py)

Paso 6: Endpoint de salud (routes/health.py)

Paso 7: Dockerfile del backend

Paso 8: Docker Compose con DynamoDB Local

Paso 9: Verificación de funcionamiento
