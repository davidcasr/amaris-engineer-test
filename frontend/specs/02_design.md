Este documento define las especificaciones técnicas para la implementación del **frontend** de la aplicación Fondos. El objetivo es construir una interfaz web funcional y simple que permita al usuario interactuar con el sistema de fondos desarrollado en el backend, incluyendo suscripciones, cancelaciones, visualización de transacciones y configuración de notificaciones.

## Stack Tecnológico

- **React** + **Vite**: Framework moderno, rápido y fácil de configurar.
- **Tailwind CSS**: Utilidades de CSS para desarrollo rápido.
- **Shadcn UI**: Librería de componentes visuales preconstruidos.
- **Fetch API**: Para consumo de endpoints REST.
- **ESLint + Prettier** (opcional): Para estilo y calidad del código.

## Guía de Diseño

- **Paleta neutra**: gris claro, azul, blanco.
- **Layout centrado** con ancho máximo de 800px.
- **Espaciado generoso** entre secciones.
- **Tipografía simple** (`sans-serif`, o Google Font como `Inter`).
- **Componentes UI** gestionados con Shadcn.

## Criterios de validación

- Todos los endpoints deben estar conectados y funcionando correctamente.
- Validación básica de formularios (campos requeridos).
- Mensajes de error y éxito visibles.
- Navegación fluida entre vistas.
- Compatible con pantallas pequeñas (no 100% mobile first, pero usable).
