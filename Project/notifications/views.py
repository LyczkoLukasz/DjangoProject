from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import Notification

# Create your views here.
@login_required
def notifications(request):

    notifications = Notification.objects.all().order_by('-created_at')
    context = {'notifications': notifications}

    return render(request, 'notifications/index.html', context)
