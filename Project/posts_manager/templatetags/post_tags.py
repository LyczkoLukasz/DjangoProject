from django import template
from django.contrib.auth.models import User
from posts_manager.models import Posts, Comments, Likes

register = template.Library()

@register.inclusion_tag('posts_manager/post_with_comments.html')
def get_post_with_comments(post_id, logged_user):

    post = Posts.objects.get(id=post_id)
    post.views += 1
    post.save()

    liked = False
    liked = Likes.objects.filter(user=logged_user, post=post).exists()

    post_comments = Comments.get_comments_for_post(post)
    
    like_count = Likes.objects.filter(post=post).count()
    comment_count = Comments.objects.filter(post=post).count()

    return {
        'post': post,
        'liked': liked,
        'comments': post_comments,
        'like_count': like_count,
        'comment_count': comment_count,
    }