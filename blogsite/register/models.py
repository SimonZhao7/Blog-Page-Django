from django.db import models
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# Create your models here.


class RegisterForm(UserCreationForm):
    email = models.EmailField()

    class Meta:
        model = User
        fields = ["email", "username", "password1", "password2"]