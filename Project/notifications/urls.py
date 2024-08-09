from django.urls import path

from . import views


urlpatterns = [
    path('', views.notifications, name='notifications'),
    # Add more URL patterns here
]