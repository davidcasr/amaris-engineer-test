import React from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { Badge } from '@/components/ui/badge';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import LoadingSpinner from '@/components/common/LoadingSpinner';
import { useTransactions } from '@/hooks';
import { formatCurrency, formatDate } from '@/lib/utils';

export default function Transactions() {
  const {
    filteredTransactions,
    filters,
    stats,
    loading,
    updateFilters,
    hasTransactions,
    hasFilteredResults,
  } = useTransactions();

  const getTransactionTypeLabel = (type) => {
    return type === 'subscribe' ? 'Suscripción' : 'Cancelación';
  };

  const getTransactionTypeBadge = (type) => {
    return type === 'subscribe' 
      ? <Badge variant="default">Suscripción</Badge>
      : <Badge variant="secondary">Cancelación</Badge>;
  };

  if (loading) {
    return (
      <div className="container-app">
        <h1 className="text-3xl font-bold mb-6">Historial de Transacciones</h1>
        <LoadingSpinner message="Cargando historial de transacciones..." />
      </div>
    );
  }

  return (
    <div className="container-app">
      <h1 className="text-3xl font-bold mb-2">Historial de Transacciones</h1>
      <p className="text-muted-foreground mb-6">
        Revisa todas tus transacciones de suscripciones y cancelaciones de fondos.
      </p>

      {/* Estadísticas */}
      {stats && (
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
          <Card>
            <CardContent className="pt-6">
              <div className="text-2xl font-bold">{stats.total}</div>
              <p className="text-xs text-muted-foreground">Total Transacciones</p>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="pt-6">
              <div className="text-2xl font-bold text-green-600">{stats.subscriptions}</div>
              <p className="text-xs text-muted-foreground">Suscripciones</p>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="pt-6">
              <div className="text-2xl font-bold text-orange-600">{stats.unsubscriptions}</div>
              <p className="text-xs text-muted-foreground">Cancelaciones</p>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="pt-6">
              <div className="text-2xl font-bold">{formatCurrency(stats.totalAmount)}</div>
              <p className="text-xs text-muted-foreground">Monto Total</p>
            </CardContent>
          </Card>
        </div>
      )}

      {/* Filtros */}
      <Card className="mb-6">
        <CardHeader>
          <CardTitle>Filtros</CardTitle>
          <CardDescription>Filtra las transacciones por tipo</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="flex gap-4">
            <div className="w-48">
              <Select value={filters.type} onValueChange={(value) => updateFilters({ type: value })}>
                <SelectTrigger>
                  <SelectValue placeholder="Tipo de transacción" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">Todas</SelectItem>
                  <SelectItem value="subscribe">Suscripciones</SelectItem>
                  <SelectItem value="unsubscribe">Cancelaciones</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Tabla de transacciones */}
      <Card>
        <CardHeader>
          <CardTitle>Transacciones</CardTitle>
          <CardDescription>
            {filteredTransactions.length} transacciones {filters.type !== 'all' ? `(filtradas por ${filters.type === 'subscribe' ? 'suscripciones' : 'cancelaciones'})` : ''}
          </CardDescription>
        </CardHeader>
        <CardContent>
          {!hasFilteredResults ? (
            <div className="text-center py-8">
              <p className="text-muted-foreground">
                {!hasTransactions 
                  ? 'No tienes transacciones registradas aún.'
                  : 'No hay transacciones que coincidan con el filtro seleccionado.'
                }
              </p>
            </div>
          ) : (
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Fecha</TableHead>
                  <TableHead>Tipo</TableHead>
                  <TableHead>Fondo</TableHead>
                  <TableHead>Monto</TableHead>
                  <TableHead>ID Transacción</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {filteredTransactions.map((transaction) => (
                  <TableRow key={transaction.transactionId}>
                    <TableCell>
                      {formatDate(transaction.timestamp)}
                    </TableCell>
                    <TableCell>
                      {getTransactionTypeBadge(transaction.type)}
                    </TableCell>
                    <TableCell className="font-medium">
                      {transaction.fundName || transaction.fundId}
                    </TableCell>
                    <TableCell>
                      {formatCurrency(transaction.amount)}
                    </TableCell>
                    <TableCell className="text-xs text-muted-foreground font-mono">
                      {transaction.transactionId}
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          )}
        </CardContent>
      </Card>
    </div>
  );
}