# 📊 Plataforma de Fondos de Inversión

> **Prueba técnica como ingeniero de software para Amaris Consulting**

## 📖 Descripción del Proyecto

La **Plataforma de Fondos de Inversión** es una aplicación web completa que permite a los usuarios gestionar sus inversiones en fondos. El sistema ofrece funcionalidades para visualizar fondos disponibles, realizar suscripciones, gestionar transacciones y configurar notificaciones.

### 🎯 Características Principales

- **Gestión de Fondos**: Visualización de fondos disponibles con información detallada
- **Suscripciones**: Sistema de suscripción y cancelación de fondos de inversión
- **Transacciones**: Historial completo de transacciones del usuario
- **Configuración**: Gestión de preferencias de notificaciones
- **API RESTful**: Backend robusto con documentación automática
- **Interfaz Moderna**: Frontend responsivo con diseño intuitivo

## 🛠️ Stack Tecnológico

### Backend

- **FastAPI** - Framework web moderno y rápido para Python
- **DynamoDB** - Base de datos NoSQL de Amazon Web Services
- **Pydantic** - Validación de datos y serialización
- **Uvicorn** - Servidor ASGI de alto rendimiento

### Frontend

- **React 18** - Biblioteca de JavaScript para interfaces de usuario
- **Vite** - Herramienta de construcción rápida para desarrollo
- **Tailwind CSS** - Framework de CSS utilitario
- **Shadcn/UI** - Componentes de UI modernos y accesibles
- **React Router** - Enrutamiento del lado del cliente

### Infraestructura

- **Docker** - Containerización de aplicaciones
- **Docker Compose** - Orquestación de múltiples contenedores
- **Nginx** - Servidor web y proxy reverso

## 🏗️ Arquitectura general del sistema

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│                 │    │                 │    │                 │
│    Frontend     │────│     Backend     │────│    DynamoDB     │
│   (React/Nginx) │    │    (FastAPI)    │    │     (Local)     │
│   Puerto: 3000  │    │   Puerto: 8001  │    │   Puerto: 8000  │
│                 │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Comunicación entre Servicios

- **Frontend ↔ Backend**: API REST con proxy Nginx
- **Backend ↔ DynamoDB**: Cliente AWS SDK
- **Docker Network**: Comunicación interna entre contenedores

## 📋 Prerequisitos

Antes de ejecutar el proyecto, asegúrate de tener instalado:

- **Docker** (versión 20.10 o superior)
- **Puertos disponibles**: 3000, 8000, 8001

## 🚀 Inicio Rápido

### 1. Clonar el Repositorio

```bash
git clone <repository-url>
cd amaris-engineer-test
```

### 2. Levantar todos los Servicios

```bash
# Construir y ejecutar todos los contenedores
docker-compose up -d

# Ver logs en tiempo real
docker-compose logs -f
```

### 3. Acceder a la Aplicación

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8001

### 4. Comandos Útiles

```bash
# Detener todos los servicios
docker-compose down

# Reconstruir imágenes
docker-compose build

# Ver estado de contenedores
docker-compose ps

# Logs de un servicio específico
docker-compose logs -f frontend
docker-compose logs -f backend
```

## 📁 Estructura del Proyecto

```
amaris-engineer-test/
├── backend/                 # API Backend (FastAPI)
│   ├── app/
│   │   ├── config.py       # Configuración de la aplicación
│   │   ├── main.py         # Punto de entrada FastAPI
│   │   ├── models/         # Modelos de datos Pydantic
│   │   ├── routes/         # Endpoints de la API
│   │   ├── services/       # Lógica de negocio
│   │   └── database/       # Configuración DynamoDB
│   ├── tests/              # Pruebas unitarias e integración
│   ├── Dockerfile          # Imagen Docker del backend
│   └── requirements.txt    # Dependencias Python
│
├── frontend/               # Aplicación Frontend (React)
│   ├── src/
│   │   ├── components/     # Componentes React reutilizables
│   │   ├── pages/          # Páginas principales
│   │   ├── hooks/          # Custom hooks
│   │   ├── context/        # Context API para estado global
│   │   ├── api/            # Cliente HTTP y servicios
│   │   └── styles/         # Estilos globales CSS
│   ├── public/             # Archivos estáticos
│   ├── Dockerfile          # Imagen Docker del frontend
│   ├── nginx.conf          # Configuración Nginx
│   └── package.json        # Dependencias Node.js
│
├── infrastructure/         # Infraestructura como Código
│   └── cloudformation/     # Templates de AWS CloudFormation
│       └── template.yaml   # Definición de recursos AWS
│
├── docs/                   # Documentación del proyecto
├── docker-compose.yml      # Orquestación de servicios
└── README.md              # Documentación principal
```

## 📚 Documentación de la API

El backend genera automáticamente documentación interactiva de la API:

### 🔗 Enlaces de Documentación

- **Swagger UI**: http://localhost:8001/docs
- **ReDoc**: http://localhost:8001/redoc

### 📊 Endpoints Principales

- `GET /api/v1/funds/` - Obtener fondos disponibles
- `POST /api/v1/subscribe/` - Suscribirse a un fondo
- `POST /api/v1/unsubscribe/` - Cancelar suscripción
- `GET /api/v1/transactions/` - Historial de transacciones
- `GET /api/v1/health/` - Estado del sistema

## ⚙️ Configuración

### Variables de Entorno

#### Backend

```env
DYNAMODB_ENDPOINT=http://dynamodb:8000
AWS_REGION=us-west-2
AWS_ACCESS_KEY_ID=dummy
AWS_SECRET_ACCESS_KEY=dummy
ENVIRONMENT=development
ENABLE_AUTO_DB_INIT=true
```

#### Frontend

```env
VITE_API_URL=http://localhost:8001
NODE_ENV=production
```

### Configuración de Puertos

- **Frontend**: `3000:80` (puerto host:contenedor)
- **Backend**: `8001:8000`
- **DynamoDB**: `8000:8000`

### Personalización

- Modificar `docker-compose.yml` para cambiar puertos
- Ajustar `frontend/.env` para diferentes entornos
- Configurar `backend/app/config.py` para parámetros del sistema

Made with ❤️ by @davidcasr
