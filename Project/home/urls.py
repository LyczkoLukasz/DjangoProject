from django.urls import path
from django.views.generic.base import RedirectView

from . import views

urlpatterns = [
    #after redirecting from urls.py in Project, this is the first view that is called
    path('home/', views.home, name='home'),
    path('profile/', views.profile, name='profile'),

]