from django.db import models
from home.models import User
from django.db.models import Count


# Create your models here.

class Posts(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author', null=True ) #related_name post_user to list all his posts
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=1000)
    #post images here 
    likes = models.IntegerField(default=0)
    #comments counter replaced with annotate in line 23
    views = models.IntegerField(default=0)


    def __str__(self):
        return f'Post {self.title} created by {self.user} at {self.created_at}.'
    
    def get_Posts(specific_authors):
        posts = Posts.objects.filter(author__in=specific_authors).annotate(comment_count=Count('comments')).order_by('-created_at')
        return posts
    
class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user', null=True)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name='comments', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.CharField(max_length=500)

    def __str__(self):
        return f'Comment created by {self.user} on post {self.post} at {self.created_at}.'
    
    def get_comments_for_post(post, limit=5, offset=0):
        comments = Comments.objects.filter(post=post).order_by('-created_at')[offset:offset+limit]
        return comments