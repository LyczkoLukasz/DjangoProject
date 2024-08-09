from django.shortcuts import render
from .models import Posts, Comments

# Create your views here.


def posts_index(request):
    posts = Posts.objects.all().order_by('-post_created_at')
    context = {'posts': posts}
    return render(request, 'posts_manager/posts_index.html', context)
