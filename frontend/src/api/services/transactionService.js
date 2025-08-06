import apiClient from '../client.js';
import { ENDPOINTS, buildEndpoint } from '../endpoints.js';

export class TransactionService {
  
  /**
   * Obtener transacciones de un usuario
   * @param {string} userId - ID del usuario
   * @param {Object} filters - Filtros opcionales (tipo, fecha, etc.)
   * @returns {Promise<Array>} Lista de transacciones
   */
  async getUserTransactions(userId, filters = {}) {
    try {
      const params = {
        userId,
        ...filters
      };
      
      const response = await apiClient.get(ENDPOINTS.TRANSACTIONS, params);
      return response.transactions || [];
    } catch (error) {
      console.error('Error al obtener transacciones:', error);
      throw error;
    }
  }

  /**
   * Obtener transacciones por tipo
   * @param {string} userId - ID del usuario
   * @param {string} type - Tipo de transacción ('subscribe' | 'unsubscribe')
   * @returns {Promise<Array>} Lista de transacciones filtradas
   */
  async getTransactionsByType(userId, type) {
    try {
      const filters = { type };
      return await this.getUserTransactions(userId, filters);
    } catch (error) {
      console.error(`Error al obtener transacciones de tipo ${type}:`, error);
      throw error;
    }
  }

  /**
   * Obtener transacciones de un período específico
   * @param {string} userId - ID del usuario
   * @param {string} startDate - Fecha de inicio (ISO string)
   * @param {string} endDate - Fecha de fin (ISO string)
   * @returns {Promise<Array>} Lista de transacciones en el período
   */
  async getTransactionsByDateRange(userId, startDate, endDate) {
    try {
      const filters = {
        startDate,
        endDate
      };
      
      return await this.getUserTransactions(userId, filters);
    } catch (error) {
      console.error('Error al obtener transacciones por fecha:', error);
      throw error;
    }
  }

  /**
   * Obtener estadísticas de transacciones del usuario
   * @param {string} userId - ID del usuario
   * @returns {Promise<Object>} Estadísticas de transacciones
   */
  async getTransactionStats(userId) {
    try {
      const transactions = await this.getUserTransactions(userId);
      
      const stats = {
        total: transactions.length,
        subscriptions: transactions.filter(t => t.type === 'subscribe').length,
        unsubscriptions: transactions.filter(t => t.type === 'unsubscribe').length,
        totalAmount: transactions.reduce((sum, t) => sum + (t.amount || 0), 0),
        lastTransaction: transactions.length > 0 ? transactions[0] : null
      };
      
      return stats;
    } catch (error) {
      console.error('Error al calcular estadísticas:', error);
      throw error;
    }
  }
}

// Instancia singleton del servicio
export const transactionService = new TransactionService();
export default transactionService;