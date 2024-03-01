from django.db import models

# Create your models here.
class Customer(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=30, null=True)
    password = models.CharField(max_length=30, null=True)
    email = models.EmailField(null=True)
    name = models.CharField(max_length=30, null=True)
    surname = models.CharField(max_length=30, null=True)
    date_of_birth = models.DateField(null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
