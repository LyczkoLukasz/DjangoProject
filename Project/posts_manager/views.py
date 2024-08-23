from django.shortcuts import render
from .models import Posts, Comments

# Create your views here.

#this is not used right now 
def posts_index(request):
    posts = Posts.objects.all()#.order_by('-post_created_at')
    print(posts)  # Debugging line
    context = {'posts': posts}
    return render(request, 'home/posts.html', context)
