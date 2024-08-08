from django import template
from friendship_manager.models import Friendship
from django.db.models import Q


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