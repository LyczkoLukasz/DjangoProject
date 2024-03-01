from django.shortcuts import render
from .models import Customer

def home(request):
    return render(request, 'home/main.html')

def profile(request, pk):
    customer = Customer.objects.get(id=pk)
    context = {'customer': customer}
    return render(request, 'home/profile.html', context)