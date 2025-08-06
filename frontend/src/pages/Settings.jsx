import React, { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { useUser, useNotifications } from '@/hooks';
import { settingsService } from '@/api/services';
import { CheckCircle } from 'lucide-react';

export default function Settings() {
  const { user, loading, actions } = useUser();
  const { showSuccess, showError } = useNotifications();
  const [saving, setSaving] = useState(false);

  const handleSave = async () => {
    try {
      setSaving(true);
      
      const result = await actions.updateNotificationType(user.notificationType);
      
      if (result.success) {
        showSuccess(
          `Las notificaciones se enviarán por ${user.notificationType === 'email' ? 'correo electrónico' : 'SMS'}.`,
          { title: '¡Configuración guardada!' }
        );
      } else {
        showError(result.error);
      }
      
    } catch (err) {
      showError(`Error al guardar la configuración: ${err.message}`);
      console.error('Error saving settings:', err);
    } finally {
      setSaving(false);
    }
  };

  const notificationOptions = settingsService.getAvailableNotificationTypes();

  return (
    <div className="container-app">
      <h1 className="text-3xl font-bold mb-2">Configuración</h1>
      <p className="text-muted-foreground mb-6">
        Personaliza tus preferencias de notificaciones y otras configuraciones de la cuenta.
      </p>



      {/* Configuración de Notificaciones */}
      <Card className="mb-6">
        <CardHeader>
          <CardTitle>Notificaciones</CardTitle>
          <CardDescription>
            Configura cómo deseas recibir las notificaciones cuando te suscribas a un fondo.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="notification-type">Tipo de notificación</Label>
              <Select 
                value={user.notificationType} 
                onValueChange={(value) => actions.updateNotificationType(value)}
                disabled={loading || saving}
              >
                <SelectTrigger id="notification-type">
                  <SelectValue placeholder="Selecciona el tipo de notificación" />
                </SelectTrigger>
                <SelectContent>
                  {notificationOptions.map((option) => (
                    <SelectItem key={option.value} value={option.value}>
                      {option.label}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            <div className="text-sm text-muted-foreground">
              <p>
                • <strong>Correo electrónico:</strong> Recibirás notificaciones en tu email registrado.
              </p>
              <p>
                • <strong>SMS:</strong> Recibirás notificaciones por mensaje de texto.
              </p>
            </div>

            <Button 
              onClick={handleSave} 
              disabled={loading || saving}
              className="w-full sm:w-auto"
            >
              {saving ? 'Guardando...' : 'Guardar Configuración'}
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Información de la cuenta */}
      <Card>
        <CardHeader>
          <CardTitle>Información de la Cuenta</CardTitle>
          <CardDescription>
            Detalles básicos de tu cuenta en la plataforma.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            <div>
              <Label className="text-sm font-medium">ID de Usuario</Label>
              <p className="text-sm text-muted-foreground font-mono">
                {user.id}
              </p>
            </div>
            
            <div>
              <Label className="text-sm font-medium">Saldo Disponible</Label>
              <p className="text-sm font-semibold">
                {new Intl.NumberFormat('es-CO', { style: 'currency', currency: 'COP' }).format(user.balance)}
              </p>
            </div>
            
            <div>
              <Label className="text-sm font-medium">Tipo de Notificación Actual</Label>
              <p className="text-sm">
                {user.notificationType === 'email' ? 'Correo electrónico' : 'SMS'}
              </p>
            </div>

            <div>
              <Label className="text-sm font-medium">Estado de la Cuenta</Label>
              <div className="flex items-center gap-2">
                <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                <span className="text-sm">Activa</span>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}