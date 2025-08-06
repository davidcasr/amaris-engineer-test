Esta guía define los pasos necesarios para construir completamente la lógica del backend de la aplicación de fondos, utilizando FastAPI, Pydantic, DynamoDB Local y buenas prácticas de arquitectura limpia.

El objetivo es dejar el backend listo para producción, con todas las funcionalidades operativas, respetando las reglas de validación, consistencia de datos y manejo adecuado de errores.

Paso 1: Crear modelos base con Pydantic (models/)
Define los esquemas de entrada y salida.

```
models/
├── fund.py
├── user.py
├── subscription.py
└── transaction.py
```

Paso 2: Configurar acceso a la base de datos (database/)
Configura boto3 para conectarse con DynamoDB Local usando variables de entorno en .env.

Paso 3: Crear archivos de inicialización de tablas (database/init.py)
Permite crear las tablas necesarias para desarrollo local automáticamente si no existen.

Paso 4: Implementar servicios de negocio (services/)
Cada archivo de servicio encapsula operaciones sobre una entidad, validaciones y lógica de negocio.

Paso 5: Crear rutas funcionales (routes/)
Define endpoints agrupados por entidad (funds, subscriptions, transactions, notifications, etc.).

Paso 6: Definir excepciones personalizadas (exceptions.py)
Centraliza los errores comunes y personaliza los mensajes según el tipo de problema (404, 409, etc.).

Paso 7: Crear modelos de entrada (DTOs)
Define modelos específicos para operaciones como suscripciones, cancelaciones y configuraciones de usuario.

Paso 8: Conectar todas las rutas en main.py
Registra los routers en la aplicación FastAPI, agrupando por entidad.

Paso 9: Crear función de notificación dinámica
En services/notification_service.py o similar:

```
def send_notification(notification_type: str, recipient: str, message: str):
    if notification_type == "email":
        print(f"[Email] Sending to {recipient}: {message}")
    elif notification_type == "sms":
        print(f"[SMS] Sending to {recipient}: {message}")
    else:
        raise ValueError("Unsupported notification type")
```

El tipo (email o sms) será obtenido desde los datos del usuario (notificationType).

Paso 10: Implementar lógica completa de los endpoints Implementar:

```
1. GET /funds → Listado general.
2. POST /subscribe → Validación de fondos, saldo, duplicidad.
3. POST /unsubscribe → Cancelación segura, reintegro si aplica.
4. GET /transactions → Historial del usuario.
5. POST /settings/notifications → Cambio de tipo de notificación.
```

Paso 11: Validar todas las respuestas con response_model
Todas las respuestas deben estar tipadas con modelos de salida (Fund, Transaction, etc.).

Paso 12: Agregar manejo de errores global
Agrega un @app.exception_handler en main.py para interceptar errores inesperados y retornar respuestas consistentes.

Paso 13: Revisión final de calidad y endpoints
Verifica que:

1. Todos los endpoints están implementados según lo definido en los specs.

   - Se utilizan modelos Pydantic en entradas y salidas.
   - El manejo de errores es claro, explícito y consistente.
   - La lógica de negocio respeta reglas como:
     - Validación de saldo
     - Registro de transacciones
     - Notificación según preferencia del usuario

2. Revisa en Swagger: http://localhost:8001/docs
3. Refactoriza código duplicado, comentarios obsoletos, y estructuras poco claras.
