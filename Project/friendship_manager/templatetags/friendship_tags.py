
from django import template
from friendship_manager.models import Friendship


register = template.Library()


@register.simple_tag
def getListOfSendedInvitations(self, user):
    return Friendship.objects.filter(to_user=user, is_Friend=False)
    
@register.simple_tag
def getListOfReceivedInvitations(self, user):
    return Friendship.objects.filter(from_user=user, is_Friend=False)
    
@register.simple_tag
def getListOfFriends(self, user):
    return Friendship.objects.filter(from_user=user, is_Friend=True).filter(to_user=user, is_Friend=True)
    