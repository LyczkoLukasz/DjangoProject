from django.db import models
from home.models import User
from django.utils.translation import gettext_lazy as _

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


class Notification(models.Model):
    class NotificationType(models.TextChoices):
        GENERAL_NOTIFICATION = 'GN', _("General notification")
        NEW_POST = 'NP', _("New Post")
        NEW_COMMENT = 'NC', _("New Comment")
        NEW_LIKE = 'NL', _("New Like")
        NEW_FRIENDSHIP_STATUS = 'FC', _("Friendship status changed")

    #user is a user who will receive the notification
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=100)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    #type defines what kind of notification it is
    type = models.CharField(max_length=2, choices=NotificationType.choices, default=NotificationType.GENERAL_NOTIFICATION)
    #hook_id is used to store the id of the object that the notification is related to
    hook_id = models.CharField(max_length=100, blank=True, null=True)


    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Sending notifications to user in real-time through Django layers - Web sockets
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
    
            f'notifications_{self.user.id}',
            {
                'type': 'send_notification',
                'notification': {
                    'id': self.id,
                    'title': self.title,
                    'body': self.body,
                    'type': self.type,
                    'hook_id': self.hook_id,
                    'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                }
            }
        )
    
    def getNumberOfUnreadNotifications(user_provided):
        return Notification.objects.filter(user=user_provided, is_read=False).count()
    
    
    
    def getTypesOfNotifications(notifications):
        types = []
        for notification in notifications:
            types.append(notification.type)
        return types
    
