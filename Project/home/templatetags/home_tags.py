from django import template
from friendship_manager.models import Friendship
from notifications.models import Notification
from django.db.models import Q

from notifications.models import Notification

register = template.Library()


@register.inclusion_tag('home/buttons/cancel.html')
def getSentInvitation(user, userProfilePK):
    #user is a user who is logged in
    #userProfilePK is a user who is a profile owner
    return {'friend_request': Friendship.objects.get(from_user=user, to_user=userProfilePK, is_Friend=False)}
    
@register.inclusion_tag('home/buttons/accept_decline.html')
def getReceivedInvitation(user, userProfilePK):
    #user is a user who is logged in
    #userProfilePK is a user who is a profile owner
    return {'friend_request': Friendship.objects.get(from_user=userProfilePK, to_user=user, is_Friend=False)}
    
@register.inclusion_tag('home/buttons/kill.html')
def getFriend(user, userProfilePK):
    #user is a user who is logged in
    #userProfilePK is a user who is a profile owner
    return {'friend_request': Friendship.objects.get( Q(from_user=user) & Q(to_user=userProfilePK) | Q(from_user=userProfilePK) & Q(to_user=user), is_Friend=True)}

@register.inclusion_tag('home/base/latest_notifications.html')
def latest_notifications(user):
    notifications = Notification.objects.filter(user=user).order_by('-created_at')[:4]
    return {'notifications': notifications}

@register.inclusion_tag('home/base/banner.html')
def numberOfUnreadNotifications(user):
    numberOfNotifications = Notification.getNumberOfUnreadNotifications(user)
    return {'numberOfNotifications': numberOfNotifications}