from home.models import User
from django.db import models

# Create your models here.

class Friendship(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='from_user')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='to_user')
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    is_Friend = models.BooleanField(default=False)

    class Meta:
        unique_together = ('from_user', 'to_user')

    def __str__(self):
        if self.is_Friend:
            return f'{self.from_user} is friends with {self.to_user}'
        elif not self.is_Friend:
            return f'{self.from_user} is not friends with {self.to_user}'
        return 'there is missing data in this object'