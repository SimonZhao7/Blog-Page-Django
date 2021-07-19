from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as user_login, logout as user_logout
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.forms import AuthenticationForm
from django.conf import settings
from django.contrib import messages
from .models import CustomUser
from .forms import RegisterForm, ChangeUsernameForm, ChangePasswordForm, ChangeEmailForm, ChangeProfilePicForm
import os
# Create your views here.



@login_required
def profile(request, username):
    user = get_object_or_404(CustomUser, username=username)
    return render(request, 'account/profile.html', {"viewed_user": user})


def login(request):
    if request.user.is_authenticated:
        return redirect('/' + request.user.username)
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = CustomUser.objects.get(username=form.cleaned_data["username"])
            user_login(request, user)
            return redirect('/' + user.username)
    return render(request, "account/login.html", {"form": form})


@login_required
def logout(request):
    if request.method == 'POST':
        user_logout(request)
        return redirect('/')
    return render(request, 'account/logout.html')


def register(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.profile_picture = '/static/images/no-profile.png'
            account.save()
            return redirect('/')
    return render(request, "account/register.html", {'form': form})


@login_required
def change_username(request):
    form = ChangeUsernameForm(user=request.user)
    if request.method == 'POST':
        form = ChangeUsernameForm(request.POST, user=request.user)
        if form.is_valid():
            request.user.username = form.cleaned_data['username']
            request.user.save()
            messages.success(request, 'You have successfully changed your username')
    return render(request, "account/change_user.html", {'form': form})


@login_required
def change_password(request):
    form = ChangePasswordForm(user=request.user)
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST, user=request.user)
        if form.is_valid():
            request.user.set_password(form.cleaned_data['new_password'])
            request.user.save()

            # prevent logout
            user_login(request, request.user)
            messages.success(request, 'You have successfully changed your password')
    return render(request, 'account/change_password.html', {'form': form})


@login_required
def change_email(request):
    form = ChangeEmailForm(user=request.user)
    if request.method == 'POST':
        form = ChangeEmailForm(request.POST, user=request.user)
        if form.is_valid():
            request.user.email = form.cleaned_data['email']
            request.user.save()
            messages.success(request, 'You have successfully changed your email')
    return render(request, 'account/change_email.html', {'form': form})


@login_required
def change_profile_pic(request):
    form = ChangeProfilePicForm()
    if request.method == 'POST':
        form = ChangeProfilePicForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['profile_pic']
            fs = FileSystemStorage()

            # save file to media and update user
            saved_filepath = fs.save(os.path.join('profile_pictures', file.name), file)
            request.user.profile_picture = settings.MEDIA_URL + saved_filepath
            request.user.save()

            messages.success(request, 'You have successfully changed your profile picture')
    return render(request, 'account/change_profile_pic.html', {'form': form})