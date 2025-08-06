import React from 'react';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import LoadingSpinner from '@/components/common/LoadingSpinner';
import { useFunds, useNotifications } from '@/hooks';
import { formatCurrency, formatDateShort } from '@/lib/utils';

export default function MyFunds() {
  const { userFunds, loading, unsubscribing, unsubscribeFromFund } = useFunds();
  const { showWarning } = useNotifications();

  const handleUnsubscribe = async (fundId) => {
    const confirmed = await new Promise((resolve) => {
      const id = showWarning(
        '¿Estás seguro de que deseas cancelar la suscripción a este fondo?',
        {
          title: 'Confirmar cancelación',
          autoClose: false,
          actions: [
            {
              label: 'Cancelar',
              onClick: () => resolve(false),
            },
            {
              label: 'Confirmar',
              variant: 'destructive',
              onClick: () => resolve(true),
            },
          ],
        }
      );
    });

    if (confirmed) {
      await unsubscribeFromFund(fundId);
    }
  };

  if (loading) {
    return (
      <div className="container-app">
        <h1 className="text-3xl font-bold mb-6">Mis Fondos</h1>
        <LoadingSpinner message="Cargando tus fondos suscritos..." />
      </div>
    );
  }

  return (
    <div className="container-app">
      <h1 className="text-3xl font-bold mb-2">Mis Fondos</h1>
      <p className="text-muted-foreground mb-6">
        Fondos a los que actualmente estás suscrito. Aquí puedes gestionar tus suscripciones.
      </p>

      {userFunds.length === 0 ? (
        <Card>
          <CardContent className="pt-6 text-center">
            <p className="text-muted-foreground mb-4">
              No tienes fondos suscritos en este momento.
            </p>
            <Button variant="outline" onClick={() => window.location.href = '/funds'}>
              Explorar Fondos Disponibles
            </Button>
          </CardContent>
        </Card>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {userFunds.map((fund) => (
            <Card key={fund.fundId} className="card-shadow">
              <CardHeader>
                <div className="flex justify-between items-start">
                  <CardTitle className="text-lg">{fund.name}</CardTitle>
                  <Badge variant={fund.category === 'FPV' ? 'default' : 'secondary'}>
                    {fund.category}
                  </Badge>
                </div>
                <CardDescription>
                  Suscrito desde {formatDateShort(fund.subscribedAt)}
                </CardDescription>
              </CardHeader>
              
              <CardContent>
                <div className="space-y-3">
                  <div>
                    <p className="text-sm text-muted-foreground">Monto mínimo</p>
                    <p className="text-lg font-semibold">{formatCurrency(fund.minAmount)}</p>
                  </div>
                  
                  <div>
                    <p className="text-sm text-muted-foreground">Estado</p>
                    <Badge variant="outline" className="text-green-600 border-green-600">
                      Activo
                    </Badge>
                  </div>

                  {fund.description && (
                    <p className="text-sm text-muted-foreground">{fund.description}</p>
                  )}
                </div>
              </CardContent>

              <CardFooter>
                <Button 
                  variant="destructive" 
                  className="w-full" 
                  onClick={() => handleUnsubscribe(fund.fundId)}
                  disabled={unsubscribing === fund.fundId}
                >
                  {unsubscribing === fund.fundId ? 'Cancelando...' : 'Cancelar Suscripción'}
                </Button>
              </CardFooter>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}