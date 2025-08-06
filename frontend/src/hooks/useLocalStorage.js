import { useState, useEffect, useCallback } from 'react';

/**
 * Hook personalizado para manejar localStorage de forma reactiva
 */
export function useLocalStorage(key, initialValue) {
  // Estado para almacenar el valor
  const [storedValue, setStoredValue] = useState(() => {
    try {
      // Obtener del localStorage por la clave
      const item = window.localStorage.getItem(key);
      // Parsear el JSON almacenado o devolver el valor inicial
      return item ? JSON.parse(item) : initialValue;
    } catch (error) {
      console.error(`Error al leer localStorage para la clave "${key}":`, error);
      return initialValue;
    }
  });

  // Función para actualizar el valor
  const setValue = useCallback((value) => {
    try {
      // Permitir que value sea una función para tener la misma API que useState
      const valueToStore = value instanceof Function ? value(storedValue) : value;
      
      // Guardar en el estado
      setStoredValue(valueToStore);
      
      // Guardar en localStorage
      window.localStorage.setItem(key, JSON.stringify(valueToStore));
    } catch (error) {
      console.error(`Error al guardar en localStorage para la clave "${key}":`, error);
    }
  }, [key, storedValue]);

  // Función para remover el valor
  const removeValue = useCallback(() => {
    try {
      window.localStorage.removeItem(key);
      setStoredValue(initialValue);
    } catch (error) {
      console.error(`Error al remover localStorage para la clave "${key}":`, error);
    }
  }, [key, initialValue]);

  // Escuchar cambios en localStorage desde otras pestañas
  useEffect(() => {
    const handleStorageChange = (e) => {
      if (e.key === key && e.newValue !== null) {
        try {
          setStoredValue(JSON.parse(e.newValue));
        } catch (error) {
          console.error(`Error al parsear localStorage para la clave "${key}":`, error);
        }
      }
    };

    window.addEventListener('storage', handleStorageChange);
    
    return () => {
      window.removeEventListener('storage', handleStorageChange);
    };
  }, [key]);

  return [storedValue, setValue, removeValue];
}

/**
 * Hook para manejar preferencias del usuario en localStorage
 */
export function useUserPreferences() {
  const [preferences, setPreferences, removePreferences] = useLocalStorage('userPreferences', {
    theme: 'light',
    language: 'es',
    notificationSettings: {
      showSuccessMessages: true,
      showErrorMessages: true,
      autoCloseDelay: 5000,
    },
    tableSettings: {
      itemsPerPage: 10,
      sortOrder: 'desc',
    },
  });

  const updatePreference = useCallback((key, value) => {
    setPreferences(prev => ({
      ...prev,
      [key]: value,
    }));
  }, [setPreferences]);

  const updateNestedPreference = useCallback((parentKey, childKey, value) => {
    setPreferences(prev => ({
      ...prev,
      [parentKey]: {
        ...prev[parentKey],
        [childKey]: value,
      },
    }));
  }, [setPreferences]);

  const resetPreferences = useCallback(() => {
    removePreferences();
  }, [removePreferences]);

  return {
    preferences,
    updatePreference,
    updateNestedPreference,
    resetPreferences,
  };
}

export default useLocalStorage;