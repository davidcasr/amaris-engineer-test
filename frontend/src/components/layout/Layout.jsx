import React from 'react';
import NavBar from './NavBar';

export default function Layout({ children }) {
  return (
    <div className="min-h-screen bg-background">
      <NavBar />
      <main className="pb-8">
        {children}
      </main>
      
      {/* Footer */}
      <footer className="border-t bg-muted/30">
        <div className="container-app py-6">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <div className="text-sm text-muted-foreground">
              © 2024 {import.meta.env.VITE_APP_NAME || 'Plataforma de Fondos'}. 
              Todos los derechos reservados.
            </div>
            <div className="text-sm text-muted-foreground mt-2 md:mt-0">
              Versión {import.meta.env.VITE_APP_VERSION || '1.0.0'}
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}