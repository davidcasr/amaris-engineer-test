import React from 'react';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Alert, AlertDescription } from '@/components/ui/alert';
import LoadingSpinner from '@/components/common/LoadingSpinner';
import { useFunds } from '@/hooks';
import { formatCurrency } from '@/lib/utils';

export default function Funds() {
  const { 
    funds, 
    loading, 
    subscribing, 
    subscribeToFund, 
    loadFunds,
    isSubscribedToFund 
  } = useFunds();

  const handleSubscribe = async (fundId) => {
    await subscribeToFund(fundId);
  };

  if (loading) {
    return (
      <div className="container-app">
        <h1 className="text-3xl font-bold mb-6">Fondos Disponibles</h1>
        <LoadingSpinner message="Cargando fondos disponibles..." />
      </div>
    );
  }

  return (
    <div className="container-app">
      <h1 className="text-3xl font-bold mb-2">Fondos Disponibles</h1>
      <p className="text-muted-foreground mb-6">
        Explora nuestra selección de fondos de inversión y suscríbete al que mejor se adapte a tus necesidades.
      </p>

      {funds.length === 0 ? (
        <Card>
          <CardContent className="pt-6">
            <p className="text-center text-muted-foreground">
              No hay fondos disponibles en este momento.
            </p>
          </CardContent>
        </Card>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {funds.map((fund) => (
            <Card key={fund.fundId} className="card-shadow hover:shadow-lg transition-shadow">
              <CardHeader>
                <div className="flex justify-between items-start">
                  <CardTitle className="text-lg">{fund.name}</CardTitle>
                  <Badge variant={fund.category === 'FPV' ? 'default' : 'secondary'}>
                    {fund.category}
                  </Badge>
                </div>
                <CardDescription>
                  Fondo de inversión {fund.category === 'FPV' ? 'Pensión Voluntaria' : 'Inversión Colectiva'}
                </CardDescription>
              </CardHeader>
              
              <CardContent>
                <div className="space-y-3">
                  <div>
                    <p className="text-sm text-muted-foreground">Monto mínimo</p>
                    <p className="text-lg font-semibold">{formatCurrency(fund.minAmount)}</p>
                  </div>
                  
                  {fund.description && (
                    <p className="text-sm text-muted-foreground">{fund.description}</p>
                  )}
                </div>
              </CardContent>

              <CardFooter>
                <Button 
                  className="w-full" 
                  onClick={() => handleSubscribe(fund.fundId)}
                  disabled={subscribing === fund.fundId || isSubscribedToFund(fund.fundId)}
                  variant={isSubscribedToFund(fund.fundId) ? 'secondary' : 'default'}
                >
                  {subscribing === fund.fundId 
                    ? 'Suscribiendo...' 
                    : isSubscribedToFund(fund.fundId) 
                    ? 'Ya suscrito' 
                    : 'Suscribirse'
                  }
                </Button>
              </CardFooter>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}