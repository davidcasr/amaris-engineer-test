import { useState, useEffect, useCallback, useMemo } from 'react';
import { transactionService } from '@/api/services';
import { useUser } from '@/context/UserContext';
import { useApi } from './useApi';

/**
 * Hook personalizado para manejar transacciones del usuario
 */
export function useTransactions() {
  const [transactions, setTransactions] = useState([]);
  const [filters, setFilters] = useState({
    type: 'all', // 'all', 'subscribe', 'unsubscribe'
    startDate: null,
    endDate: null,
  });
  const { user } = useUser();
  const { execute, loading } = useApi();

  // Cargar transacciones del usuario
  const loadTransactions = useCallback(async () => {
    const result = await execute(
      () => transactionService.getUserTransactions(user.id),
      { showErrorNotification: false }
    );

    if (result.success) {
      setTransactions(result.data);
    }

    return result;
  }, [execute, user.id]);

  // Cargar estadísticas de transacciones
  const loadStats = useCallback(async () => {
    const result = await execute(
      () => transactionService.getTransactionStats(user.id),
      { showErrorNotification: false }
    );

    return result;
  }, [execute, user.id]);

  // Aplicar filtros a las transacciones
  const filteredTransactions = useMemo(() => {
    let filtered = [...transactions];

    // Filtrar por tipo
    if (filters.type !== 'all') {
      filtered = filtered.filter(transaction => transaction.type === filters.type);
    }

    // Filtrar por fecha
    if (filters.startDate) {
      filtered = filtered.filter(transaction => 
        new Date(transaction.timestamp) >= new Date(filters.startDate)
      );
    }

    if (filters.endDate) {
      filtered = filtered.filter(transaction => 
        new Date(transaction.timestamp) <= new Date(filters.endDate)
      );
    }

    // Ordenar por fecha (más reciente primero)
    filtered.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));

    return filtered;
  }, [transactions, filters]);

  // Estadísticas calculadas
  const stats = useMemo(() => {
    const subscriptions = transactions.filter(t => t.type === 'subscribe');
    const unsubscriptions = transactions.filter(t => t.type === 'unsubscribe');
    const totalAmount = transactions.reduce((sum, t) => sum + (t.amount || 0), 0);

    return {
      total: transactions.length,
      subscriptions: subscriptions.length,
      unsubscriptions: unsubscriptions.length,
      totalAmount,
      lastTransaction: transactions.length > 0 ? transactions[0] : null,
      thisMonth: transactions.filter(t => {
        const transactionDate = new Date(t.timestamp);
        const now = new Date();
        return transactionDate.getMonth() === now.getMonth() && 
               transactionDate.getFullYear() === now.getFullYear();
      }).length,
    };
  }, [transactions]);

  // Actualizar filtros
  const updateFilters = useCallback((newFilters) => {
    setFilters(prev => ({ ...prev, ...newFilters }));
  }, []);

  // Limpiar filtros
  const clearFilters = useCallback(() => {
    setFilters({
      type: 'all',
      startDate: null,
      endDate: null,
    });
  }, []);

  // Obtener transacciones por fondo
  const getTransactionsByFund = useCallback((fundId) => {
    return transactions.filter(transaction => transaction.fundId === fundId);
  }, [transactions]);

  // Obtener última transacción por tipo
  const getLastTransactionByType = useCallback((type) => {
    const filtered = transactions.filter(t => t.type === type);
    return filtered.length > 0 ? filtered[0] : null;
  }, [transactions]);

  // Cargar datos iniciales
  useEffect(() => {
    loadTransactions();
  }, [loadTransactions]);

  return {
    // Estado
    transactions,
    filteredTransactions,
    filters,
    stats,
    loading,

    // Acciones
    loadTransactions,
    loadStats,
    updateFilters,
    clearFilters,

    // Utilidades
    getTransactionsByFund,
    getLastTransactionByType,

    // Datos derivados
    hasTransactions: transactions.length > 0,
    hasFilteredResults: filteredTransactions.length > 0,
  };
}

export default useTransactions;