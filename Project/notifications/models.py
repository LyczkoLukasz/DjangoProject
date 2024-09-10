from django.db import models
from home.models import User

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

# Create your models here.

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=100)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Wysyłanie powiadomienia do użytkownika w czasie rzeczywistym
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'notifications_{self.user.id}',
            {
                'type': 'send_notification',
                'notification': {
                    'title': self.title,
                    'body': self.body,
                    'created_at': str(self.created_at),
                }
            }
        )
    
    def getNumberOfUnreadNotifications(user_provided):
        
        return Notification.objects.filter(user=user_provided, is_read=False).count()
    
