from django import template
from notifications.models import Notification

register = template.Library()

@register.inclusion_tag('notifications/listNotifications.html')
def getListOfNotifitcations(user):

    #all notifacations for user to display on notification page
    notifications = Notification.objects.filter(user=user).order_by('-created_at')
    return {'notifications': notifications, 'user': user}