import React from 'react';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';
import { Button } from '@/components/ui/button';
import { useNotifications, NOTIFICATION_TYPES } from '@/context/NotificationContext';
import { CheckCircle, AlertCircle, AlertTriangle, Info, X } from 'lucide-react';
import { cn } from '@/lib/utils';

// Configuración de iconos y estilos por tipo
const notificationConfig = {
  [NOTIFICATION_TYPES.SUCCESS]: {
    icon: CheckCircle,
    variant: 'default',
    className: 'border-green-200 bg-green-50 text-green-800 dark:border-green-800 dark:bg-green-950 dark:text-green-200',
    iconClassName: 'text-green-600 dark:text-green-400',
  },
  [NOTIFICATION_TYPES.ERROR]: {
    icon: AlertCircle,
    variant: 'destructive',
    className: 'border-red-200 bg-red-50 text-red-800 dark:border-red-800 dark:bg-red-950 dark:text-red-200',
    iconClassName: 'text-red-600 dark:text-red-400',
  },
  [NOTIFICATION_TYPES.WARNING]: {
    icon: AlertTriangle,
    variant: 'default',
    className: 'border-yellow-200 bg-yellow-50 text-yellow-800 dark:border-yellow-800 dark:bg-yellow-950 dark:text-yellow-200',
    iconClassName: 'text-yellow-600 dark:text-yellow-400',
  },
  [NOTIFICATION_TYPES.INFO]: {
    icon: Info,
    variant: 'default',
    className: 'border-blue-200 bg-blue-50 text-blue-800 dark:border-blue-800 dark:bg-blue-950 dark:text-blue-200',
    iconClassName: 'text-blue-600 dark:text-blue-400',
  },
};

function NotificationItem({ notification }) {
  const { removeNotification } = useNotifications();
  const config = notificationConfig[notification.type] || notificationConfig[NOTIFICATION_TYPES.INFO];
  const Icon = config.icon;

  const handleClose = () => {
    removeNotification(notification.id);
  };

  return (
    <Alert className={cn(
      'relative pr-12 mb-3 transition-all duration-300 ease-in-out',
      config.className
    )}>
      <Icon className={cn('h-4 w-4', config.iconClassName)} />
      
      {notification.title && (
        <AlertTitle className="mb-1">
          {notification.title}
        </AlertTitle>
      )}
      
      <AlertDescription>
        {notification.message}
      </AlertDescription>

      <Button
        variant="ghost"
        size="icon"
        className="absolute top-2 right-2 h-6 w-6 hover:bg-black/10 dark:hover:bg-white/10"
        onClick={handleClose}
      >
        <X className="h-3 w-3" />
      </Button>
    </Alert>
  );
}

export default function NotificationToast() {
  const { notifications } = useNotifications();

  if (notifications.length === 0) {
    return null;
  }

  return (
    <div className="fixed top-4 right-4 z-50 w-96 max-w-[90vw]">
      <div className="space-y-2">
        {notifications.map((notification) => (
          <NotificationItem
            key={notification.id}
            notification={notification}
          />
        ))}
      </div>
    </div>
  );
}