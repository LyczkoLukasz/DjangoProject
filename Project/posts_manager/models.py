from django.db import models
from home.models import User


# Create your models here.

class Posts(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author', null=True ) #related_name post_user to list all his posts
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100)
    content = models.TextField(max_length=1000)
    #post images here 
    likes = models.IntegerField(default=0)
    comments = models.IntegerField(default=0)
    views = models.IntegerField(default=0)


    def __str__(self):
        return f'Post {self.title} created by {self.user} at {self.created_at}.'
    
    def get_Posts():
        posts = Posts.objects.all().order_by('-created_at')
        return posts
    
class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user', null=True)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name='post', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField(max_length=500)

    def __str__(self):
        return f'Comment created by {self.user} on post {self.post} at {self.created_at}.'