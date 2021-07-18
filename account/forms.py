from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import CustomUser


class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = CustomUser
        fields = ["email", "username", "password1", "password2"]


class ChangeUsernameForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    username = forms.CharField(label='New Username', max_length=150)
    password = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        password = self.cleaned_data['password']

        if not authenticate(username=self.user.username, password=password):
            raise ValidationError('Incorrect Password')

