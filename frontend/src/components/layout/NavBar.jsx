import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { cn } from '@/lib/utils';
import { Card } from '@/components/ui/card';
import { Building2, Wallet, History, Settings } from 'lucide-react';

const navigation = [
  {
    name: 'Fondos Disponibles',
    href: '/funds',
    icon: Building2,
  },
  {
    name: 'Mis Fondos',
    href: '/my-funds',
    icon: Wallet,
  },
  {
    name: 'Transacciones',
    href: '/transactions',
    icon: History,
  },
  {
    name: 'Configuración',
    href: '/settings',
    icon: Settings,
  },
];

export default function NavBar() {
  const location = useLocation();

  return (
    <nav className="sticky top-0 z-50 bg-white border-b shadow-sm backdrop-blur-sm">
      <div className="container-app">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link to="/funds" className="flex items-center space-x-2">
            <Building2 className="h-8 w-8 text-primary" />
            <span className="text-xl font-bold">
              {import.meta.env.VITE_APP_NAME || 'Plataforma de Fondos'}
            </span>
          </Link>

          {/* Navigation Links - Desktop */}
          <div className="hidden md:flex space-x-1">
            {navigation.map((item) => {
              const isActive = location.pathname === item.href;
              const Icon = item.icon;
              
              return (
                <Link
                  key={item.name}
                  to={item.href}
                  className={cn(
                    'flex items-center space-x-2 px-3 py-2 rounded-md text-sm font-medium transition-colors',
                    isActive
                      ? 'bg-primary text-primary-foreground'
                      : 'text-muted-foreground hover:text-foreground hover:bg-accent'
                  )}
                >
                  <Icon className="h-4 w-4" />
                  <span>{item.name}</span>
                </Link>
              );
            })}
          </div>
        </div>

        {/* Navigation Links - Mobile */}
        <div className="md:hidden pb-4">
          <div className="grid grid-cols-2 gap-2">
            {navigation.map((item) => {
              const isActive = location.pathname === item.href;
              const Icon = item.icon;
              
              return (
                <Link key={item.name} to={item.href}>
                  <Card className={cn(
                    'p-3 transition-colors',
                    isActive 
                      ? 'bg-primary text-primary-foreground' 
                      : 'hover:bg-accent'
                  )}>
                    <div className="flex items-center space-x-2">
                      <Icon className="h-4 w-4" />
                      <span className="text-sm font-medium">{item.name}</span>
                    </div>
                  </Card>
                </Link>
              );
            })}
          </div>
        </div>
      </div>
    </nav>
  );
}