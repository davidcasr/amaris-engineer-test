import React, { createContext, useContext, useReducer, useCallback } from 'react';

// Estado inicial
const initialState = {
  notifications: [],
  maxNotifications: 5,
};

// Tipos de notificaciones
export const NOTIFICATION_TYPES = {
  SUCCESS: 'success',
  ERROR: 'error',
  WARNING: 'warning',
  INFO: 'info',
};

// Acciones
const NOTIFICATION_ACTIONS = {
  ADD_NOTIFICATION: 'ADD_NOTIFICATION',
  REMOVE_NOTIFICATION: 'REMOVE_NOTIFICATION',
  CLEAR_ALL: 'CLEAR_ALL',
};

// Reducer
function notificationReducer(state, action) {
  switch (action.type) {
    case NOTIFICATION_ACTIONS.ADD_NOTIFICATION:
      const newNotifications = [action.payload, ...state.notifications];
      
      // Limitar el número máximo de notificaciones
      return {
        ...state,
        notifications: newNotifications.slice(0, state.maxNotifications),
      };

    case NOTIFICATION_ACTIONS.REMOVE_NOTIFICATION:
      return {
        ...state,
        notifications: state.notifications.filter(
          notification => notification.id !== action.payload
        ),
      };

    case NOTIFICATION_ACTIONS.CLEAR_ALL:
      return {
        ...state,
        notifications: [],
      };

    default:
      return state;
  }
}

// Crear contexto
const NotificationContext = createContext(undefined);

// Provider del contexto
export function NotificationProvider({ children }) {
  const [state, dispatch] = useReducer(notificationReducer, initialState);

  // Función para generar ID único
  const generateId = () => `notification-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;

  // Agregar notificación
  const addNotification = useCallback((notification) => {
    const id = generateId();
    const newNotification = {
      id,
      type: NOTIFICATION_TYPES.INFO,
      autoClose: true,
      duration: 5000,
      ...notification,
      timestamp: new Date(),
    };

    dispatch({
      type: NOTIFICATION_ACTIONS.ADD_NOTIFICATION,
      payload: newNotification,
    });

    // Auto-remover si está configurado
    if (newNotification.autoClose) {
      setTimeout(() => {
        removeNotification(id);
      }, newNotification.duration);
    }

    return id;
  }, []);

  // Remover notificación
  const removeNotification = useCallback((id) => {
    dispatch({
      type: NOTIFICATION_ACTIONS.REMOVE_NOTIFICATION,
      payload: id,
    });
  }, []);

  // Limpiar todas las notificaciones
  const clearAll = useCallback(() => {
    dispatch({ type: NOTIFICATION_ACTIONS.CLEAR_ALL });
  }, []);

  // Funciones de conveniencia para diferentes tipos
  const showSuccess = useCallback((message, options = {}) => {
    return addNotification({
      type: NOTIFICATION_TYPES.SUCCESS,
      message,
      title: 'Éxito',
      ...options,
    });
  }, [addNotification]);

  const showError = useCallback((message, options = {}) => {
    return addNotification({
      type: NOTIFICATION_TYPES.ERROR,
      message,
      title: 'Error',
      autoClose: false, // Los errores no se cierran automáticamente
      ...options,
    });
  }, [addNotification]);

  const showWarning = useCallback((message, options = {}) => {
    return addNotification({
      type: NOTIFICATION_TYPES.WARNING,
      message,
      title: 'Advertencia',
      ...options,
    });
  }, [addNotification]);

  const showInfo = useCallback((message, options = {}) => {
    return addNotification({
      type: NOTIFICATION_TYPES.INFO,
      message,
      title: 'Información',
      ...options,
    });
  }, [addNotification]);

  const contextValue = {
    notifications: state.notifications,
    addNotification,
    removeNotification,
    clearAll,
    showSuccess,
    showError,
    showWarning,
    showInfo,
  };

  return (
    <NotificationContext.Provider value={contextValue}>
      {children}
    </NotificationContext.Provider>
  );
}

// Hook personalizado para usar el contexto
export function useNotifications() {
  const context = useContext(NotificationContext);
  
  if (context === undefined) {
    throw new Error('useNotifications debe ser usado dentro de un NotificationProvider');
  }
  
  return context;
}

export default NotificationContext;