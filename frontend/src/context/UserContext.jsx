import React, { createContext, useContext, useReducer, useEffect } from 'react';
import { settingsService } from '@/api/services';

// Estados iniciales
const initialState = {
  user: {
    id: import.meta.env.VITE_DEV_USER_ID || 'user-123',
    balance: 1000000, // Saldo simulado en COP
    notificationType: 'email',
  },
  loading: false,
  error: null,
};

// Tipos de acciones
const USER_ACTIONS = {
  SET_LOADING: 'SET_LOADING',
  SET_USER: 'SET_USER',
  UPDATE_NOTIFICATION_TYPE: 'UPDATE_NOTIFICATION_TYPE',
  UPDATE_BALANCE: 'UPDATE_BALANCE',
  SET_ERROR: 'SET_ERROR',
  CLEAR_ERROR: 'CLEAR_ERROR',
};

// Reducer para manejar el estado del usuario
function userReducer(state, action) {
  switch (action.type) {
    case USER_ACTIONS.SET_LOADING:
      return {
        ...state,
        loading: action.payload,
      };

    case USER_ACTIONS.SET_USER:
      return {
        ...state,
        user: { ...state.user, ...action.payload },
        error: null,
      };

    case USER_ACTIONS.UPDATE_NOTIFICATION_TYPE:
      return {
        ...state,
        user: {
          ...state.user,
          notificationType: action.payload,
        },
      };

    case USER_ACTIONS.UPDATE_BALANCE:
      return {
        ...state,
        user: {
          ...state.user,
          balance: action.payload,
        },
      };

    case USER_ACTIONS.SET_ERROR:
      return {
        ...state,
        error: action.payload,
        loading: false,
      };

    case USER_ACTIONS.CLEAR_ERROR:
      return {
        ...state,
        error: null,
      };

    default:
      return state;
  }
}

// Crear contexto
const UserContext = createContext(undefined);

// Provider del contexto
export function UserProvider({ children }) {
  const [state, dispatch] = useReducer(userReducer, initialState);

  // Cargar configuración del usuario al iniciar
  useEffect(() => {
    // Configuración inicial del usuario ya está en initialState
    // No necesitamos cargar desde el backend por ahora
  }, []);

  const updateNotificationType = async (notificationType) => {
    try {
      dispatch({ type: USER_ACTIONS.SET_LOADING, payload: true });
      
      await settingsService.updateNotificationSettings(state.user.id, notificationType);
      
      dispatch({ 
        type: USER_ACTIONS.UPDATE_NOTIFICATION_TYPE, 
        payload: notificationType 
      });
      
      return { success: true };
    } catch (error) {
      dispatch({ type: USER_ACTIONS.SET_ERROR, payload: error.message });
      return { success: false, error: error.message };
    } finally {
      dispatch({ type: USER_ACTIONS.SET_LOADING, payload: false });
    }
  };

  const updateBalance = (newBalance) => {
    dispatch({ type: USER_ACTIONS.UPDATE_BALANCE, payload: newBalance });
  };

  const clearError = () => {
    dispatch({ type: USER_ACTIONS.CLEAR_ERROR });
  };

  const contextValue = {
    ...state,
    actions: {
      updateNotificationType,
      updateBalance,
      clearError,
    },
  };

  return (
    <UserContext.Provider value={contextValue}>
      {children}
    </UserContext.Provider>
  );
}

// Hook personalizado para usar el contexto
export function useUser() {
  const context = useContext(UserContext);
  
  if (context === undefined) {
    throw new Error('useUser debe ser usado dentro de un UserProvider');
  }
  
  return context;
}

export default UserContext;