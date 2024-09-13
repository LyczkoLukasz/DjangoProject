from django.urls import path
from . import views
from home.views import get_more_comments
from home.views import toggle_like


urlpatterns = [
    path('', views.notifications, name='notifications'),
    path('get_more_comments/<int:post_id>/<int:offset>/', get_more_comments, name='get_more_comments'),
    path('toggle_like/<int:post_id>/', toggle_like, name='toggle_like')
    # Add more URL patterns here
]