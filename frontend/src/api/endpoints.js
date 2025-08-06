// Definición centralizada de endpoints del backend

export const ENDPOINTS = {
  // Fondos
  FUNDS: '/api/v1/funds/',
  
  // Suscripciones
  SUBSCRIBE: '/api/v1/subscribe/',
  UNSUBSCRIBE: '/api/v1/unsubscribe/',
  
  // Transacciones
  TRANSACTIONS: '/api/v1/transactions/',
  
  // Configuración
  SETTINGS: {
    NOTIFICATIONS: '/api/v1/settings/notifications/',
  },
  
  // Salud del sistema
  HEALTH: '/api/v1/health/',
};

// Helpers para construir URLs dinámicas
export const buildEndpoint = {
  transactions: (userId) => `${ENDPOINTS.TRANSACTIONS}?userId=${userId}`,
  userFunds: (userId) => `${ENDPOINTS.FUNDS}?userId=${userId}`,
};

export default ENDPOINTS;