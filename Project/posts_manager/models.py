from django.db import models
from home.models import User


# Create your models here.

class Posts(models.Model):
    post_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_user') #related_name post_user to list all his posts
    post_created_at = models.DateTimeField(auto_now_add=True)
    post_title = models.CharField(max_length=100)
    post_content = models.TextField(max_length=1000)
    #post images here 
    post_likes = models.IntegerField(default=0)
    post_comments = models.IntegerField(default=0)
    post_views = models.IntegerField(default=0)


    def __str__(self):
        return f'Post {self.post_title} created by {self.post_user} at {self.post_created_at}.'
    
class Comments(models.Model):
    comment_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_user')
    comment_post = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name='comment_post')
    comment_created_at = models.DateTimeField(auto_now_add=True)
    comment_content = models.TextField(max_length=500)

    def __str__(self):
        return f'Comment created by {self.comment_user} on post {self.comment_post} at {self.comment_created_at}.'