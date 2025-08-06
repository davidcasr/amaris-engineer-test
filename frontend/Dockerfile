# Multi-stage build para optimizar el tamaño de la imagen

# Etapa 1: Build
FROM node:18-alpine AS build

# Establecer directorio de trabajo
WORKDIR /app

# Copiar archivos de dependencias
COPY package*.json ./

# Instalar dependencias (usar npm install en lugar de npm ci)
RUN npm install

# Copiar código fuente
COPY . .

# Construir la aplicación para producción
RUN npm run build

# Etapa 2: Production
FROM nginx:1.25-alpine AS production

# Copiar archivos construidos desde la etapa de build
COPY --from=build /app/dist /usr/share/nginx/html

# Copiar configuración personalizada de Nginx
COPY nginx.conf /etc/nginx/nginx.conf

# Exponer puerto 80
EXPOSE 80

# Comando para iniciar Nginx
CMD ["nginx", "-g", "daemon off;"]