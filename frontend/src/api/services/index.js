// Exportación centralizada de todos los servicios de API

export { fundService } from './fundService.js';
export { transactionService } from './transactionService.js';
export { settingsService } from './settingsService.js';

// Re-exportar cliente y utilidades
export { default as apiClient } from '../client.js';
export { ApiError } from '../client.js';
export { ENDPOINTS, buildEndpoint } from '../endpoints.js';

// Importar para usar en el objeto services
import { fundService } from './fundService.js';
import { transactionService } from './transactionService.js';
import { settingsService } from './settingsService.js';

// Servicios disponibles como objeto
export const services = {
  funds: fundService,
  transactions: transactionService,
  settings: settingsService,
};

export default services;