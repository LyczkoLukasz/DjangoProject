from django.db import models

from home.models import User
from django.db import models

# Create your models here.

class Friendship(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='from_user')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='to_user')
    created_at = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    is_Friend = models.BooleanField(default=False)

    class Meta:
        unique_together = ('from_user', 'to_user')

    def __str__(self):
        return f'{self.from_user} is friends with {self.to_user}'