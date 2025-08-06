import apiClient from '../client.js';
import { ENDPOINTS } from '../endpoints.js';

export class SettingsService {
  
  /**
   * Actualizar configuración de notificaciones del usuario
   * @param {string} userId - ID del usuario
   * @param {string} notificationType - Tipo de notificación ('email' | 'sms')
   * @returns {Promise<Object>} Respuesta de la actualización
   */
  async updateNotificationSettings(userId, notificationType) {
    try {
      if (!['email', 'sms'].includes(notificationType)) {
        throw new Error('Tipo de notificación inválido. Debe ser "email" o "sms"');
      }

      const payload = {
        userId,
        notificationType
      };
      
      const response = await apiClient.post(ENDPOINTS.SETTINGS.NOTIFICATIONS, payload);
      return response;
    } catch (error) {
      console.error('Error al actualizar configuración de notificaciones:', error);
      throw error;
    }
  }

  /**
   * Validar configuración de notificaciones
   * @param {string} notificationType - Tipo de notificación a validar
   * @returns {boolean} True si es válido
   */
  validateNotificationType(notificationType) {
    return ['email', 'sms'].includes(notificationType);
  }

  /**
   * Obtener tipos de notificación disponibles
   * @returns {Array} Lista de tipos disponibles
   */
  getAvailableNotificationTypes() {
    return [
      { value: 'email', label: 'Correo electrónico' },
      { value: 'sms', label: 'SMS' }
    ];
  }
}

// Instancia singleton del servicio
export const settingsService = new SettingsService();
export default settingsService;