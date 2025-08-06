Desarrollar una interfaz web básica que permita a los usuarios interactuar con la API REST del backend de fondos. La aplicación debe ser funcional, clara y minimalista, enfocada en cumplir los requerimientos sin complejidad innecesaria.

## Tecnologías a utilizar

- React con Vite (cliente rápido y liviano)
- Tailwind CSS (opcional, para estilo rápido y utilitario)
- Fetch API (consumo directo de endpoints)
- React Router (si se requieren múltiples vistas)
- ESLint + Prettier (formato y buenas prácticas, opcional)

## Estructura de carpetas

```
frontend/
├── public/                       # Archivos estáticos
├── src/
│   ├── api/                      # Lógica para llamadas HTTP (fetch/Axios)
│   ├── components/               # Componentes reutilizables
│   ├── pages/                    # Vistas principales (Home, Settings, etc.)
│   ├── styles/                   # Estilos globales (opcional)
│   ├── ui/                       # Componentes de Shadcn UI
│   ├── App.jsx                   # Ruteo principal
│   └── main.jsx                  # Entry point de React
├── .env                          # Variables de entorno
├── Dockerfile                    # Dockerfile para contenedor del frontend
├── docker-compose.yml            # Opcional: para levantar frontend junto con backend
├── index.html                    # HTML base
├── tailwind.config.js            # Configuración de Tailwind CSS
├── postcss.config.js             # Configuración de PostCSS
├── vite.config.js                # Configuración de Vite
└── package.json                  # Dependencias y scripts de npm

```

## Funcionalidades del Frontend

### 1. Página Principal: Fondos disponibles

- Mostrar fondos (`GET /funds`)
- Botón para suscribirse (`POST /subscribe`)

### 2. Página: Mis Fondos

- Mostrar lista de fondos suscritos
- Botón para cancelar (`POST /unsubscribe`)

### 3. Página: Transacciones

- Mostrar transacciones por usuario (`GET /transactions?userId=...`)

### 4. Página: Configuración de Notificaciones

- Selector entre Email o SMS (`POST /settings/notifications`)

## Componentes básicos esperados

| Componente         | Descripción                                 |
| ------------------ | ------------------------------------------- |
| `FundCard`         | Muestra info de un fondo + botón suscribir  |
| `NotificationForm` | Formulario de configuración de notificación |
| `TransactionTable` | Tabla de movimientos                        |
| `NavBar`           | Navegación entre vistas                     |

## Recomendaciones para desarrollo

- Usa useState, useEffect y fetch sin librerías extra.
- Reutiliza componentes como FundCard, TransactionRow, FormInput.
- Utiliza archivos .env para guardar la URL del backend (por ejemplo: VITE_API_URL=http://localhost:8001).
- Si usas Tailwind, puedes hacerlo usando CSS plano para simplificar aún más.

## Guía de Inicio

Paso 1: Crear estructura de carpetas mínima
Paso 2: Dockerfile para inicializar el proyecto Vite
Paso 3: Crear el archivo docker-compose.yml para desarrollo
Paso 4: Incluir archivo necesarios dento de .dockerignore
Paso 5: Verificación de funcionamiento del ambiente basico
