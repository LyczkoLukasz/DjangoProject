from django.shortcuts import render

def home(request):
    return render(request, 'home/main.html')

def profile(request):
    return render(request, 'home/profile.html')