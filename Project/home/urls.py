from django.urls import path
from django.views.generic.base import RedirectView


from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.LoginPage, name='login'),
    #path('register/', views.register, name='register'),
    #after redirecting from urls.py in Project, this is the first view that is called
    path('home/', views.home, name='home'),
    #path('profile/<str:pk>', views.profile, name='profile'),
    path('', RedirectView.as_view(url='/home/'))

]