from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = Profile
        fields = ["email", "username", "password1", "password2"]