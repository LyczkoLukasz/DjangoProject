from django.urls import path
from django.views.generic.base import RedirectView


from . import views

urlpatterns = [
    path('login/', views.LoginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerPage, name='register'),
    #after redirecting from urls.py in Project, this is the first view that is called
    path('home/', views.home, name='home'),
    path('profile/<str:pk>', views.profile, name='profile'),
    path('profile/', views.myProfile, name='myProfile'),
    path('', RedirectView.as_view(url='/home/')),
    path('profile-edit/', views.profileEdit, name='profileEdit'),
    path('friends/', views.friends, name='friends')

]