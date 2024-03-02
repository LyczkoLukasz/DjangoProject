from django.contrib import admin
from django import forms
from django.contrib.auth.hashers import make_password
# Register your models here.
from .models import User

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'

    def save(self, commit=True):
        user = super().save(commit=False)
        user.password = make_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class UserAdmin(admin.ModelAdmin):
    form = UserForm

admin.site.register(User, UserAdmin)