from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from .models import Friendship
from home.models import User

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
        return JsonResponse({'status': 'ok', 'message': 'Zaproszenie zaakceptowane!'})
    return JsonResponse({'status': 'error', 'message': 'Nieprawidłowe żądanie.'}, status=400)