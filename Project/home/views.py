from django.shortcuts import render, redirect
from .models import User
from django.contrib import messages
from django.contrib.auth import get_user_model, decorators, login, logout
from django.contrib.auth.hashers import make_password


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
    return render(request, 'home/main.html')

@decorators.login_required(login_url='login')
def profile(request, pk):
    user = User.objects.get(id=pk)
    context = {'user': user}
    return render(request, 'home/profile.html', context)

def registerPage(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password1')
        User = get_user_model()

        if User.objects.filter(email=email).exists() or User.objects.filter(username=username).exists():
            messages.error(request, 'Email or username already exists')
        else:
            user = User.objects.create(username=username, email=email, password=make_password(password))
            user.save()
            messages.success(request, 'Account was created for ' + username)
            return redirect('home')

    return render(request, 'home/signup_page.html')
