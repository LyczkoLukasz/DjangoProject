
from django import template
from friendship_manager.models import Friendship
from django.db.models import Q


register = template.Library()


@register.inclusion_tag('friendship_manager/templetags/listSended.html')
def getListOfSendedInvitations(user):
    return {'friend_requests': Friendship.objects.filter(from_user=user, is_Friend=False) }
    
@register.inclusion_tag('friendship_manager/templetags/listReceived.html')
def getListOfReceivedInvitations(user):
    return {'friend_requests': Friendship.objects.filter(to_user=user, is_Friend=False) }
    
@register.inclusion_tag('friendship_manager/templetags/listFriends.html')
def getListOfFriends(user):
    return {'friend_requests': Friendship.objects.filter( Q(from_user=user) | Q(to_user=user), is_Friend=True) }
    