from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from .models import Friendship
from home.models import User
from notifications.models import Notification

# Create your views here.
@login_required
def friends(request):
    friends = Friendship.objects.all()
    context = {'friends': friends}
    return render(request, 'friendship_manager/friends.html', context)

@login_required
def friendship_accepted(request):
    if request.method == 'POST':
        fromWho = request.POST.get('fromWho')
        toWho = request.POST.get('toWho')
        print(fromWho)
        print(toWho)

        if not fromWho:
            return JsonResponse({'status': 'error', 'message': 'Id of sender not provided.'})
        if not toWho:
            return JsonResponse({'status': 'error', 'message': 'Id of receiver not provided.'})


        sender = get_object_or_404(User, username=fromWho)
        receiver = get_object_or_404(User, username=toWho)
        try:
            friendship = Friendship.objects.get(from_user=sender , to_user=receiver)
        except:
            return JsonResponse({'status': 'error', 'message': 'Friendship not found.'})
        
        
        friendship = Friendship.objects.get(from_user=sender , to_user=receiver)
        #modify object so that attribute isFriend is set to True
        friendship.is_Friend = True
        #save object to database
        friendship.save()

        #sending a notification to the user who sent the invitation
        Notification.objects.create(user=sender, title='Invitation Accepted!', body=f'{receiver.username} accepted your invitation!', type='FC')
        return JsonResponse({'status': 'ok', 'message': 'Invite accepted!'})
    return JsonResponse({'status': 'error', 'message': 'Nieprawidłowe żądanie.'}, status=400)

@login_required
def friendship_rejected_or_killed(request):
    print('Uruchomiono funkcję friendship_rejected_or_killed')
    if request.method == 'POST':
        fromUser = request.POST.get('fromWho')
        toUser = request.POST.get('toWho')
        print(fromUser)
        print(toUser)

        if not fromUser:
            return JsonResponse({'status': 'error', 'message': 'Id of sender not provided.'})
        if not toUser:
            return JsonResponse({'status': 'error', 'message': 'Id of receiver not provided.'})


        sender = get_object_or_404(User, username=fromUser)
        receiver = get_object_or_404(User, username=toUser)
        if Friendship.objects.filter(from_user=sender , to_user=receiver).exists():
            friendship = Friendship.objects.get(from_user=sender , to_user=receiver)
        elif Friendship.objects.filter(from_user=receiver , to_user=sender).exists():
            friendship = Friendship.objects.get(from_user=receiver , to_user=sender)
        else:
            return JsonResponse({'status': 'error', 'message': 'Friendship not found.'})
        
        #delete object from database
        friendship.delete()
        #sending a notification to the user who sent the invitation
        Notification.objects.create(user=sender, title='Invitation Rejected or killed!', body=f'{receiver.username} rejected or killed your invitation!', type='FC')
        return JsonResponse({'status': 'ok', 'message': 'Deleted successfully!'})
    return JsonResponse({'status': 'error', 'message': 'Nieprawidłowe żądanie.'}, status=400)   