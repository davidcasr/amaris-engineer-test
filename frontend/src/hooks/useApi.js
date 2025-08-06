import { useState, useCallback } from 'react';
import { useNotifications } from '@/context/NotificationContext';
import { ApiError } from '@/api/client';

/**
 * Hook personalizado para manejar llamadas a la API
 * Proporciona estado de loading, error y funciones para hacer requests
 */
export function useApi() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const { showError } = useNotifications();

  const clearError = useCallback(() => {
    setError(null);
  }, []);

  const execute = useCallback(async (apiCall, options = {}) => {
    const {
      showErrorNotification = true,
      onSuccess,
      onError,
      loadingMessage,
    } = options;

    try {
      setLoading(true);
      setError(null);

      const result = await apiCall();

      if (onSuccess) {
        onSuccess(result);
      }

      return { success: true, data: result, error: null };
    } catch (err) {
      const errorMessage = err instanceof ApiError ? err.message : 'Error inesperado';
      
      setError({
        message: errorMessage,
        status: err.status || 0,
        details: err.data || {},
      });

      if (showErrorNotification) {
        showError(errorMessage);
      }

      if (onError) {
        onError(err);
      }

      return { success: false, data: null, error: err };
    } finally {
      setLoading(false);
    }
  }, [showError]);

  const executeWithCallback = useCallback(async (apiCall, successCallback, errorCallback) => {
    return execute(apiCall, {
      onSuccess: successCallback,
      onError: errorCallback,
    });
  }, [execute]);

  return {
    loading,
    error,
    execute,
    executeWithCallback,
    clearError,
  };
}

/**
 * Hook para manejar múltiples estados de API
 */
export function useApiState() {
  const [states, setStates] = useState({});

  const createApiState = useCallback((key) => {
    if (!states[key]) {
      setStates(prev => ({
        ...prev,
        [key]: {
          loading: false,
          error: null,
          data: null,
        },
      }));
    }
    return states[key] || { loading: false, error: null, data: null };
  }, [states]);

  const updateApiState = useCallback((key, updates) => {
    setStates(prev => ({
      ...prev,
      [key]: {
        ...prev[key],
        ...updates,
      },
    }));
  }, []);

  const clearApiState = useCallback((key) => {
    setStates(prev => {
      const newStates = { ...prev };
      delete newStates[key];
      return newStates;
    });
  }, []);

  return {
    states,
    createApiState,
    updateApiState,
    clearApiState,
  };
}

export default useApi;