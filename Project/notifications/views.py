from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import Notification

# Create your views here.
@login_required
def notifications(request):

    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    context = {'notifications': notifications, 'request': request}

    return render(request, 'notifications/index.html', context)

