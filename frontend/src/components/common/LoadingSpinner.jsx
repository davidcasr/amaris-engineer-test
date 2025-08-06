import React from 'react';
import { cn } from '@/lib/utils';

export default function LoadingSpinner({ 
  size = 'md', 
  className,
  message = 'Cargando...' 
}) {
  const sizeClasses = {
    sm: 'h-4 w-4',
    md: 'h-6 w-6',
    lg: 'h-8 w-8',
    xl: 'h-12 w-12',
  };

  return (
    <div className={cn('flex items-center justify-center', className)}>
      <div className="flex flex-col items-center space-y-2">
        <div
          className={cn(
            'animate-spin rounded-full border-2 border-gray-300 border-t-primary',
            sizeClasses[size]
          )}
        />
        {message && (
          <p className="text-sm text-muted-foreground">{message}</p>
        )}
      </div>
    </div>
  );
}

// Componente para página completa
export function PageLoadingSpinner({ message = 'Cargando página...' }) {
  return (
    <div className="flex items-center justify-center min-h-[400px]">
      <LoadingSpinner size="xl" message={message} />
    </div>
  );
}

// Componente para overlay
export function LoadingOverlay({ message = 'Procesando...' }) {
  return (
    <div className="absolute inset-0 bg-background/80 backdrop-blur-sm flex items-center justify-center z-50">
      <LoadingSpinner size="lg" message={message} />
    </div>
  );
}