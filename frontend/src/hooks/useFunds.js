import { useState, useEffect, useCallback } from 'react';
import { fundService } from '@/api/services';
import { useUser } from '@/context/UserContext';
import { useNotifications } from '@/context/NotificationContext';
import { useApi } from './useApi';

/**
 * Hook personalizado para manejar operaciones con fondos
 */
export function useFunds() {
  const [funds, setFunds] = useState([]);
  const [userFunds, setUserFunds] = useState([]);
  const { user } = useUser();
  const { showSuccess, showError } = useNotifications();
  const { execute, loading } = useApi();

  // Estados específicos para diferentes operaciones
  const [subscribing, setSubscribing] = useState(null);
  const [unsubscribing, setUnsubscribing] = useState(null);

  // Cargar todos los fondos disponibles
  const loadFunds = useCallback(async () => {
    const result = await execute(
      () => fundService.getAllFunds(),
      { showErrorNotification: false }
    );

    if (result.success) {
      setFunds(result.data);
    }

    return result;
  }, [execute]);

  // Cargar fondos del usuario
  const loadUserFunds = useCallback(async () => {
    const result = await execute(
      () => fundService.getUserFunds(user.id),
      { showErrorNotification: false }
    );

    if (result.success) {
      setUserFunds(result.data);
    }

    return result;
  }, [execute, user.id]);

  // Suscribirse a un fondo
  const subscribeToFund = useCallback(async (fundId) => {
    setSubscribing(fundId);

    try {
      const result = await execute(
        () => fundService.subscribeToFund(fundId, user.id),
        {
          showErrorNotification: true,
          onSuccess: () => {
            showSuccess('¡Te has suscrito exitosamente al fondo!');
            // Recargar datos
            loadFunds();
            loadUserFunds();
          },
        }
      );

      return result;
    } finally {
      setSubscribing(null);
    }
  }, [execute, user.id, showSuccess, loadFunds, loadUserFunds]);

  // Cancelar suscripción a un fondo
  const unsubscribeFromFund = useCallback(async (fundId) => {
    setUnsubscribing(fundId);

    try {
      const result = await execute(
        () => fundService.unsubscribeFromFund(fundId, user.id),
        {
          showErrorNotification: true,
          onSuccess: () => {
            showSuccess('Has cancelado la suscripción al fondo exitosamente.');
            // Recargar datos
            loadFunds();
            loadUserFunds();
          },
        }
      );

      return result;
    } finally {
      setUnsubscribing(null);
    }
  }, [execute, user.id, showSuccess, loadFunds, loadUserFunds]);

  // Verificar si el usuario está suscrito a un fondo
  const isSubscribedToFund = useCallback((fundId) => {
    return userFunds.some(fund => fund.fundId === fundId);
  }, [userFunds]);

  // Obtener información de un fondo específico
  const getFund = useCallback((fundId) => {
    return funds.find(fund => fund.fundId === fundId);
  }, [funds]);

  // Obtener fondos por categoría
  const getFundsByCategory = useCallback((category) => {
    return funds.filter(fund => fund.category === category);
  }, [funds]);

  // Cargar datos iniciales
  useEffect(() => {
    loadFunds();
    loadUserFunds();
  }, [loadFunds, loadUserFunds]);

  return {
    // Estado
    funds,
    userFunds,
    loading,
    subscribing,
    unsubscribing,

    // Acciones
    loadFunds,
    loadUserFunds,
    subscribeToFund,
    unsubscribeFromFund,

    // Utilidades
    isSubscribedToFund,
    getFund,
    getFundsByCategory,

    // Datos derivados
    totalFunds: funds.length,
    totalUserFunds: userFunds.length,
    fpvFunds: getFundsByCategory('FPV'),
    ficFunds: getFundsByCategory('FIC'),
  };
}

export default useFunds;