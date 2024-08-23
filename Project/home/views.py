from django.shortcuts import render, redirect
from .models import User
from django.contrib import messages
from django.contrib.auth import get_user_model, decorators, login, logout
from django.contrib.auth.hashers import make_password
from time import sleep
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from friendship_manager.models import Friendship
from .models import User
from django.db.models import Q
from posts_manager.models import Posts, Comments
from django.http import HttpResponseRedirect



def LoginPage(request):

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        User = get_user_model()

        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Login failed')
        except:
            messages.error(request, 'User does not exist')
    


    context = {}
    return render(request, 'home/login_page.html', context)

    
def logoutUser(request):
    logout(request)
    return redirect('home')

def home(request):
    users = User.objects.all()
    all_posts = Posts.get_Posts()

    possible_friends= Friendship.objects.filter(Q(from_user=request.user.id) | Q(to_user=request.user.id)) #lista relacji
    friends = set() #lista znajomych
    for relation in possible_friends:
        if relation.from_user == request.user and relation.is_Friend == True:
            friends.add(relation.to_user.id)
        elif relation.to_user == request.user and relation.is_Friend == True:
            friends.add(relation.from_user.id)

    posts = all_posts.filter(author__id__in=friends)
    
    if request.method == 'POST':
        response = add_post(request)
        if response:
            return response  # Zwróć odpowiedź z add_post
        else:
            return redirect('home')  # Jeśli add_post nie zwróci odpowiedzi, przekieruj na home

    context = {'users': users, 'posts': posts}
    return render(request, 'home/home.html', context)

@decorators.login_required(login_url='login')
def profile(request, pk):
    user = User.objects.get(id=pk)
    friends = Friendship.objects.filter(from_user=user)
    is_friend = Friendship.objects.filter(Q(from_user=request.user, to_user=user) | Q(from_user=user, to_user=request.user))
    is_friend_obj = is_friend.first()
    print(is_friend_obj)
    context = {'user': user, 'friends': friends, 'is_friend': is_friend_obj}
    return render(request, 'home/profile.html', context)

@decorators.login_required(login_url='login')
def myProfile(request):
    user = request.user
    context = {'user': user}
    return render(request, 'home/my_profile.html', context)

def registerPage(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password1')
        password2 = request.POST.get('password2')
        User = get_user_model()

        if password != password2:
            return redirect('register')
        else:
            if User.objects.filter(email=email).exists() or User.objects.filter(username=username).exists():
                messages.error(request, 'Email or username already exists')
            else:
                user = User.objects.create(username=username, email=email, password=make_password(password))
                user.save()
                messages.success(request, 'Account was created for ' + username)
                return redirect('home')

    return render(request, 'home/signup_page.html')

@decorators.login_required(login_url='login')
def profileEdit(request):
    if request.method == 'POST':
        user = request.user
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        date_of_birth = request.POST.get('date_of_birth')
        bio = request.POST.get('bio')

        try:
            # Check if the username is already taken by another user
            if User.objects.filter(username=username).exclude(pk=user.pk).exists():
                messages.error(request, 'Username already in use.')
            elif User.objects.filter(email=email).exclude(pk=user.pk).exists():
                messages.error(request, 'Email already in use.')
            else:
                user.first_name = first_name
                user.last_name = last_name
                user.username = username
                user.email = email
                user.date_of_birth = date_of_birth
                user.bio = bio
                user.save()
                messages.success(request, 'Profile updated')
                return redirect('profileEdit')
        except Exception as e:
            messages.error(request, 'Something went wrong, try again later :(')

        user.first_name = first_name
        user.last_name = last_name
        try:
            user.date_of_birth = date_of_birth
        except:
            print('Somting wong with date of birth')
        user.bio = bio
        user.save()
        messages.success(request, 'Profile updated')
        return redirect('profileEdit')

    else:
        pass

    return render(request, 'home/profile_edit.html')


# Handling friend requests below

@decorators.login_required
def friend_request(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        if not username:
            return JsonResponse({'status': 'error', 'message': 'Username not provided.'})
        
        user = get_object_or_404(User, username=username)
        if not Friendship.objects.filter(from_user=request.user, to_user=user).exists():
            Friendship.objects.create(from_user=request.user, to_user=user, is_Friend=False)
            return JsonResponse({'status': 'ok', 'message': 'Zaproszenie zostało wysłane.'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Oczekiwanie na odpowiedź od użytkownika.'})
    return JsonResponse({'status': 'error', 'message': 'Nieprawidłowe żądanie.'}, status=400)


@decorators.login_required
def add_post(request):
    title = request.POST.get('title')
    content = request.POST.get('content')
    user = request.user

    if title and content:
        # Tworzenie nowego posta
        post = Posts(author=user, title=title, content=content)
        post.save()

        messages.success(request, 'Post added successfully')
        return redirect('home')  # Zwróć przekierowanie po udanym dodaniu posta

    messages.error(request, 'Both title and content are required.')
    return redirect('home')