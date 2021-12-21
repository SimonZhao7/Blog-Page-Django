from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator, FileExtensionValidator
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
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']

        existing_users = CustomUser.objects.filter(username=username)

        if not authenticate(username=self.user.username, password=password):
            raise ValidationError('Incorrect Password')

        if existing_users.exists():
            raise ValidationError('This username already exists')


# this will be replaced in the future
class ChangePasswordForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    current_password = forms.CharField(widget=forms.PasswordInput())
    new_password = forms.CharField(widget=forms.PasswordInput())
    new_password2 = forms.CharField(label='Confirm New Password', widget=forms.PasswordInput())

    def clean(self):
        current_pass = self.cleaned_data['current_password']
        new_pass = self.cleaned_data['new_password']
        new_pass2 = self.cleaned_data['new_password2']

        if not authenticate(username=self.user.username, password=current_pass):
            raise ValidationError('Incorrect Password')

        if new_pass != new_pass2:
            raise ValidationError("New Passwords Don't Match")

        if len(new_pass) < 8:
            raise ValidationError('The password needs to be at least 8 characters long')


class ChangeEmailForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    email = forms.EmailField(label='New Email', validators=[EmailValidator(message='Invalid Email')])
    password = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']

        existing_users = CustomUser.objects.filter(email=email)

        if not authenticate(username=self.user.username, password=password):
            raise ValidationError('Incorrect Password')

        if existing_users.count() != 0:
            raise ValidationError('There is already an existing account with that email')


class ChangeProfilePicForm(forms.Form):
    profile_pic = forms.FileField(
        label='New Profile Picture',
        validators=[FileExtensionValidator(
                ['jpg', 'png', 'jpeg'],
                'Only .jpg and .png files are accepted'
            )
        ]
    )