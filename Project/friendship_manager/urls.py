from django.urls import path
from django.views.generic.base import RedirectView


from . import views

urlpatterns = [
    path('', views.friends, name='friends'),
    path('friendship_accepted/', views.friendship_accepted, name='friendship_accepted'),
    path('friendship_rejected_or_killed/', views.friendship_rejected_or_killed, name='friendship_rejected_or_killed'),

]