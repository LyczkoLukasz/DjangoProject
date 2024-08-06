from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Friendship

# Create your views here.
@login_required
def friends(request):
    friends = Friendship.objects.all()
    context = {'friends': friends}
    return render(request, 'friendship_manager/friends.html', context)