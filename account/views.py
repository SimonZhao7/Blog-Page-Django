from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as user_login, logout as user_logout
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.forms import AuthenticationForm
from django.conf import settings
from django.contrib import messages
from .models import CustomUser, UserFollowing, UserFriend
from .forms import RegisterForm, ChangeUsernameForm, ChangePasswordForm, ChangeEmailForm, ChangeProfilePicForm
from notifications.views import get_count
import os
# Create your views here.


@login_required
def profile(request, username):
    user = request.user
    viewed_user = get_object_or_404(CustomUser, username=username)
    followers = UserFollowing.objects.filter(following=viewed_user)
    friends = UserFriend.objects.filter(user=viewed_user)

    # checks to see if you are currently following the viewed user
    follow_value = 'Follow'
    if followers.filter(user=user).exists():
        follow_value = 'Following'

    if request.method == 'POST':
        # try to create a new object with kwargs
        new_following, created = user.userfollowing_set.get_or_create(user=user, following=viewed_user)

        # if no new object is created delete it
        if not created:
            new_following.delete()
            # if the users were friends, they will no longer be friends
            if friends.filter(friend=user).exists():
                user.userfriend_set.get(user=user, friend=viewed_user).delete()
                viewed_user.userfriend_set.get(user=viewed_user, friend=user).delete()
        else:
            # if viewed user is following you back, you two become friends
            if viewed_user.userfollowing_set.all().filter(following=user).exists():
                user.userfriend_set.create(user=user, friend=viewed_user)
                viewed_user.userfriend_set.create(user=viewed_user, friend=user)
        return redirect('account:profile', username=viewed_user.username)
    return render(
        request,
        'account/profile.html',
        {"viewed_user": viewed_user, 'follow_value': follow_value, 'followers': followers.count(), 'friends': friends.count(), 'notif_count': get_count(request)}
    )


def login(request):
    user = request.user
    if user.is_authenticated:
        return redirect('account:profile', username=user.username)
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = CustomUser.objects.get(username=form.cleaned_data["username"])
            user_login(request, user)
            return redirect('account:profile', username=user.username)
    return render(request, "account/login.html", {"form": form})


@login_required
def logout(request):
    if request.method == 'POST':
        user_logout(request)
        return redirect('account:login')
    return render(request, 'account/logout.html', {'notif_count': get_count(request)})


def register(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.profile_picture = '/media/profile_pictures/no-profile.png'
            account.save()
            return redirect('account:login')
    return render(request, "account/register.html", {'form': form})


@login_required
def change_username(request):
    user = request.user
    form = ChangeUsernameForm(user=user)
    if request.method == 'POST':
        form = ChangeUsernameForm(request.POST, user=user)
        if form.is_valid():
            user.username = form.cleaned_data['username']
            user.save()
            messages.success(request, 'You have successfully changed your username')
    return render(request, "account/change_user.html", {'form': form, 'notif_count': get_count(request)})


@login_required
def change_password(request):
    user = request.user
    form = ChangePasswordForm(user=user)
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST, user=user)
        if form.is_valid():
            user.set_password(form.cleaned_data['new_password'])
            user.save()

            # prevent logout
            user_login(request, user)
            messages.success(request, 'You have successfully changed your password')
    return render(request, 'account/change_password.html', {'form': form, 'notif_count': get_count(request)})


@login_required
def change_email(request):
    user = request.user
    form = ChangeEmailForm(user=user)
    if request.method == 'POST':
        form = ChangeEmailForm(request.POST, user=user)
        if form.is_valid():
            user.email = form.cleaned_data['email']
            user.save()
            messages.success(request, 'You have successfully changed your email')
    return render(request, 'account/change_email.html', {'form': form, 'notif_count': get_count(request)})


@login_required
def change_profile_pic(request):
    user = request.user
    form = ChangeProfilePicForm()
    if request.method == 'POST':
        form = ChangeProfilePicForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['profile_pic']
            fs = FileSystemStorage()

            # save file to media and update user
            saved_filepath = fs.save(os.path.join('profile_pictures', file.name), file)
            user.profile_picture = settings.MEDIA_URL + saved_filepath
            user.save()
            messages.success(request, 'You have successfully changed your profile picture')
    return render(request, 'account/change_profile_pic.html', {'form': form, 'notif_count': get_count(request)})