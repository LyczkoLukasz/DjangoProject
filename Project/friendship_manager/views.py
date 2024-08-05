from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def friends(request):
    return render(request, 'friendship_manager/friends.html')