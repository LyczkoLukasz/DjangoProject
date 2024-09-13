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
from django.db.models import Q, Count
from posts_manager.models import Posts, Comments, Likes
from posts_manager.models import Posts, Comments
from django.http import HttpResponseRedirect,HttpResponse
from notifications.models import Notification
from captcha.fields import CaptchaField
from django import forms


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=100)
    email = forms.EmailField()
    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())
    captcha = CaptchaField()


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

@decorators.login_required(login_url='login')
def home(request):
    users = User.objects.all()
    #posty
    #all_posts = Posts.get_Posts()
    possible_friends= Friendship.objects.filter(Q(from_user=request.user.id) | Q(to_user=request.user.id)) #lista relacji
    friends = set() #lista znajomych
    friends.add(request.user.id)
    for relation in possible_friends:
        if relation.from_user == request.user and relation.is_Friend == True:
            friends.add(relation.to_user.id)
        elif relation.to_user == request.user and relation.is_Friend == True:
            friends.add(relation.from_user.id)

    posts = Posts.get_Posts(friends)

    for post in posts:
        post.views += 1
        post.save()
    
    #comments (5 newest comments)
    posts_with_comments = []
    for post in posts:
        liked = Likes.objects.filter(user=request.user, post=post).exists()
        post_comments = Comments.get_comments_for_post(post)
        posts_with_comments.append((post, liked, post_comments))
    
    
    if request.method == 'POST':
        response = add_post(request)
        if response:
            return response  # Zwróć odpowiedź z add_post
        else:
            return redirect('home')  # Jeśli add_post nie zwróci odpowiedzi, przekieruj na home
        
    if request.method == 'POST':
        com_response = add_comment(request)
        if com_response:
            return com_response # Zwróć odpowiedź z add_comment
        else:
            return redirect('home')

    context = {'users': users, 'posts_with_comments': posts_with_comments}
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
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            password2 = form.cleaned_data.get('password2')
            User = get_user_model()

            if password != password2:
                messages.error(request, 'Passwords do not match')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists() or User.objects.filter(username=username).exists():
                    messages.error(request, 'Email or username already exists')
                else:
                    user = User.objects.create(username=username, email=email, password=make_password(password))
                    user.save()
                    messages.success(request, 'Account was created for ' + username)
                    return redirect('home')
    else:
        form = RegisterForm()

    return render(request, 'home/signup_page.html', {'form': form})

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
            print('Something wrong with date of birth')
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
            return JsonResponse({'status': 'ok', 'message': 'Invite sent!'})
        else:
            return JsonResponse({'status': 'error', 'message': "Waiting for user's response."})
    return JsonResponse({'status': 'error', 'message': 'Nieprawidłowe żądanie.'}, status=400)


@decorators.login_required
def add_post(request):
    title = request.POST.get('title')
    content = request.POST.get('content')
    user = request.user

    if title and content:
        #Limiting the title and content length
        if len(title) > 100:
            messages.error(request, 'Title cannot be longer than 100 characters.')
            return redirect('home')
        if len(content) > 1000:
            messages.error(request, 'Content cannot be longer than 1000 characters.')
            return redirect('home')
        # Tworzenie nowego posta
        post = Posts(author=user, title=title, content=content)
        post.save()

        list_of_friends = Friendship.objects.filter((Q(from_user=user) | Q(to_user=user)) & Q(is_Friend=True))
        for friend in list_of_friends:
            if friend.from_user == user:
                toWhoSendNotification = friend.to_user
            else:
                toWhoSendNotification = friend.from_user
            Notification.objects.create(user=toWhoSendNotification, title='New post!', body=f'{user.username} added a new post!', type='NP', hook_id=post.id)


        messages.success(request, 'Post added successfully')
        return redirect('home')  # Zwróć przekierowanie po udanym dodaniu posta

    messages.error(request, 'Both title and content are required.')
    return redirect('home')

@decorators.login_required
def add_comment(request):
    post_id = request.POST.get('post_id')
    post = get_object_or_404(Posts, pk=post_id)
    content = request.POST.get('add_comment')
    user = request.user

    if content:
        #Limiting the content length
        if len(content) > 500:
            messages.error(request, 'Content cannot be longer than 500 characters.')
            return redirect('home')
        # Tworzenie nowego komentarza
        comment = Comments(user=user, post=post, content=content)
        comment.save()

        messages.success(request, 'Comment added successfully')
        return redirect('home')
    
    messages.error(request, 'Comment cannot be empty.')
    return redirect('home')


def get_more_comments(request, post_id, offset):
    offset = int(offset)
    comments = Comments.objects.filter(post_id=post_id).order_by('-created_at')[offset:offset+5]
    #comments = Comments.get_comments_for_post(post_id, limit=5, offset=offset)
    comments_data = [
        {
            'user': comment.user.username,
            'content': comment.content,
            'created_at': comment.created_at.strftime('%b. %d, %Y, %-I:%M %p').replace('AM', 'a.m.').replace('PM', 'p.m.')
        }
        for comment in comments
    ]
    return JsonResponse({'comments': comments_data})

@decorators.login_required
def toggle_like(request, post_id):
    post = get_object_or_404(Posts, pk=post_id)
    user = request.user

    # Check if the like already exists
    existing_like = Likes.objects.filter(user=user, post=post).first()

    if existing_like:
        # If the like exists, delete it (unlike)
        existing_like.delete()
        liked = False
    else:
        # If the like does not exist, create it (like)
        Likes.objects.create(user=user, post=post)
        liked = True

    # Count the total number of likes for the post
    like_count = Likes.objects.filter(post=post).count()
    comment_count = Comments.objects.filter(post=post).count()

    return JsonResponse({'liked': liked, 'like_count': like_count, 'comment_count': comment_count})

def test_view(request):
    return HttpResponse(f"User ID: {request.user.id}, Username: {request.user.username}")
