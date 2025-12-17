from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .models import Notification

# Create your views here.
@login_required
def notifications(request):

    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    context = {'notifications': notifications, 'request': request}

    return render(request, 'notifications/index.html', context)

@login_required
@require_POST
def mark_notification_read(request, notification_id):
    """Mark a single notification as read"""
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.is_read = True
    notification.save()
    return JsonResponse({'status': 'success', 'notification_id': notification_id})

@login_required
@require_POST
def mark_all_notifications_read(request):
    """Mark all notifications as read for the current user"""
    Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    return JsonResponse({'status': 'success'})
