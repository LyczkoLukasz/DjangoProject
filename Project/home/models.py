from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password, is_password_usable


class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    date_of_birth = models.DateField(null=True)
    email = models.EmailField(unique=True, null=True)
    bio = models.TextField(null=True)

    def save(self, *args, **kwargs):
        if self.pk is None and not is_password_usable(self.password):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def raw_db_date_of_birth(self):
        return self.date_of_birth.strftime('%Y-%m-%d')