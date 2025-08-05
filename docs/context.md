# Plataforma de Fondos

## Propósito del proyecto

Esta es una aplicación web diseñada para gestionar la relación entre un usuario y distintos **fondos de inversión**. El sistema permite:

1. **Suscribirse a un fondo de inversión.**
2. **Cancelar la suscripción a un fondo activo.**
3. **Visualizar el historial de transacciones realizadas (suscripciones y cancelaciones).**
4. **Recibir notificaciones (por SMS o correo electrónico) al realizar suscripciones.**

---

## Alcance de la implementación

- Desarrollo de un **backend en FastAPI**, con una API REST clara, documentada y segura.
- Construcción de un **frontend en React** (con Vite), que permite al usuario interactuar con los fondos disponibles.
- Persistencia de datos mediante **DynamoDB**, simulada localmente con DynamoDB Local y preparada para producción en AWS.
- Automatización del despliegue en la nube mediante **AWS CloudFormation**, incluyendo todos los recursos necesarios.
- Uso de **Docker** y **Docker Compose** para facilitar el desarrollo y la ejecución local.
- Aplicación de buenas prácticas de ingeniería de software.

---

## Tecnologías utilizadas

| Componente          | Tecnología              | Propósito                                |
| ------------------- | ----------------------- | ---------------------------------------- |
| Backend             | FastAPI (Python)        | API REST con validaciones y lógica       |
| Base de datos       | DynamoDB (Local y AWS)  | Almacenamiento NoSQL escalable           |
| Frontend            | React + Vite            | Interfaz de usuario moderna y responsiva |
| Infraestructura     | Docker + Docker Compose | Desarrollo local, entorno reproducible   |
| Infraestructura IaC | AWS CloudFormation      | Despliegue automatizado en la nube       |
| Notificaciones      | AWS SNS                 | Envío de SMS o correos electrónicos      |

---

## Estructura del repositorio

```
fondos-app/
├── backend/
│   └── app/
│       ├── main.py
│       ├── routes.py
│       ├── services.py
│       ├── models.py
│       ├── database.py
│       └── utils.py
│   ├── Dockerfile
│   ├── requirements.txt
│   └── tests/
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── Dockerfile
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
├── infrastructure/
│   └── cloudformation/
│       ├── template.yaml
│       └── README.md
├── docker-compose.yml
└── README.md
```

---

## Modelo de datos (NoSQL - DynamoDB)

### Tabla: `Funds`

- `fundId` (string, PK): ID del fondo
- `name` (string): Nombre del fondo
- `category` (string): "FPV" o "FIC"
- `minAmount` (number): Monto mínimo de suscripción

### Tabla: `User`

- `userId` (string, PK): ID del usuario
- `balance` (number): Saldo disponible
- `notificationType` (string): "email" o "sms"

### Tabla: `UserFunds`

- `userId` (string, PK)
- `fundId` (string, SK)
- `subscribedAt` (string): Fecha de vinculación (ISO)

### Tabla: `Transactions`

- `transactionId` (string, PK)
- `userId` (string)
- `fundId` (string)
- `type` (string): "subscribe" o "unsubscribe"
- `amount` (number)
- `timestamp` (string, ISO format)

---

## 🔌 Endpoints del backend

| Método | Ruta                      | Descripción                                          |
| ------ | ------------------------- | ---------------------------------------------------- |
| GET    | `/funds`                  | Lista todos los fondos disponibles.                  |
| POST   | `/subscribe`              | Suscribe al usuario a un fondo (`fundId`).           |
| POST   | `/unsubscribe`            | Cancela la suscripción a un fondo (`fundId`).        |
| GET    | `/transactions`           | Devuelve el historial de transacciones del usuario.  |
| POST   | `/settings/notifications` | Cambia el tipo de notificación: `"email"` o `"sms"`. |

---

## Despliegue con AWS CloudFormation

La plantilla `template.yaml` despliega los siguientes recursos:

- **Lambda**: Backend empaquetado como función sin servidor.
- **API Gateway**: Exposición pública de la API REST.
- **DynamoDB**: Tablas para fondos, usuarios, transacciones y relaciones.
- **SNS**: Notificaciones vía email o SMS.
- **S3 + CloudFront**: Hosting del frontend estático.
- **IAM Roles**: Permisos entre servicios.

```bash
aws cloudformation deploy   --template-file infrastructure/cloudformation/template.yaml   --stack-name PlataformaFondosStack   --capabilities CAPABILITY_NAMED_IAM
```

---

## 🧼 Prácticas limpias aplicadas

- Separación de responsabilidades por módulo.
- Validación robusta de entradas con Pydantic.
- Manejo explícito y anticipado de errores.
- Modularidad y mantenibilidad.
- Configuración por variables de entorno.
- Pruebas automatizadas con `pytest`.
- Estilo de código uniforme (`black`, `pylint`, `eslint`).
