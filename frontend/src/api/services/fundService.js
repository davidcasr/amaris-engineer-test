import apiClient from '../client.js';
import { ENDPOINTS } from '../endpoints.js';

export class FundService {
  
  /**
   * Obtener todos los fondos disponibles
   * @returns {Promise<Array>} Lista de fondos
   */
  async getAllFunds() {
    try {
      const response = await apiClient.get(ENDPOINTS.FUNDS);
      // El backend devuelve un array directo, no un objeto con property 'funds'
      return Array.isArray(response) ? response : (response.funds || []);
    } catch (error) {
      console.error('Error al obtener fondos:', error);
      throw error;
    }
  }

  /**
   * Suscribirse a un fondo
   * @param {string} fundId - ID del fondo
   * @param {string} userId - ID del usuario (opcional, se puede obtener del contexto)
   * @returns {Promise<Object>} Respuesta de la suscripción
   */
  async subscribeToFund(fundId, userId = null) {
    try {
      const payload = { 
        fundId,
        ...(userId && { userId })
      };
      
      const response = await apiClient.post(ENDPOINTS.SUBSCRIBE, payload);
      return response;
    } catch (error) {
      console.error('Error al suscribirse al fondo:', error);
      throw error;
    }
  }

  /**
   * Cancelar suscripción a un fondo
   * @param {string} fundId - ID del fondo
   * @param {string} userId - ID del usuario (opcional)
   * @returns {Promise<Object>} Respuesta de la cancelación
   */
  async unsubscribeFromFund(fundId, userId = null) {
    try {
      const payload = { 
        fundId,
        ...(userId && { userId })
      };
      
      const response = await apiClient.post(ENDPOINTS.UNSUBSCRIBE, payload);
      return response;
    } catch (error) {
      console.error('Error al cancelar suscripción:', error);
      throw error;
    }
  }

  /**
   * Obtener fondos suscritos por un usuario
   * @param {string} userId - ID del usuario
   * @returns {Promise<Array>} Lista de fondos suscritos
   */
  async getUserFunds(userId) {
    try {
      // Nota: Este endpoint puede necesitar ajuste según la implementación del backend
      const response = await apiClient.get(`${ENDPOINTS.FUNDS}/user/${userId}`);
      return response.funds || [];
    } catch (error) {
      console.error('Error al obtener fondos del usuario:', error);
      throw error;
    }
  }
}

// Instancia singleton del servicio
export const fundService = new FundService();
export default fundService;