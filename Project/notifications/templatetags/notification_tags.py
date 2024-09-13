from django import template
from friendship_manager.models import Friendship
from django.db.models import Q

from notifications.models import Notification
from posts_manager.models import Posts


register = template.Library()

@register.inclusion_tag('notifications/listNotifications.html')
def getListOfNotifitcations(user):

    #get all notifications for the user
    notifications = Notification.objects.filter(user=user).order_by('-created_at')
    """ 
    
    
    hook_ids_posts = []
    hook_ids_profiles = []
    for notification in notifications:
        if notification.type == 'NP':
            hook_ids_posts.append(notification.hook_id)
        elif notification.type == 'FC':
            hook_ids_profiles.append(notification.hook_id)

    
    #get all posts that are related to the notifications
    posts = Posts.objects.filter(id__in=hook_ids_posts)
    """




    


    return {'notifications': notifications}