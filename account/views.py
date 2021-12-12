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
    user = get_object_or_404(CustomUser, username=username)
    followers = UserFollowing.objects.filter(following=user)
    friends = UserFriend.objects.filter(user=user)

    # checks to see if you are currently following the viewed user
    follow_value = 'Follow'
    if followers.filter(user=request.user).count() > 0:
        follow_value = 'Following'

    if request.method == 'POST':
        # try to create a new object with kwargs
        new_following = request.user.userfollowing_set.get_or_create(user=request.user, following=user)

        # if no new object is created delete it
        if not new_following[1]:
            new_following[0].delete()
            # if the users were friends, they will no longer be friends
            if friends.filter(friend=request.user).count() > 0:
                request.user.userfriend_set.get(user=request.user, friend=user).delete()
                user.userfriend_set.get(user=user, friend=request.user).delete()
        else:
            # if viewed user is following you back, you two become friends
            if user.userfollowing_set.all().filter(following=request.user).count() > 0:
                request.user.userfriend_set.create(user=request.user, friend=user)
                user.userfriend_set.create(user=user, friend=request.user)
        return redirect('/' + user.username)
    return render(
        request,
        'account/profile.html',
        {"viewed_user": user, 'follow_value': follow_value, 'followers': followers.count(), 'friends': friends.count(), 'notif_count': get_count(request)}
    )


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
    return render(request, 'account/logout.html', {'notif_count': get_count(request)})


def register(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.profile_picture = '/media/profile_pictures/no-profile.png'
            account.save()
            return redirect('/')
    return render(request, "account/register.html", {'form': form, 'notif_count': get_count(request)})


@login_required
def change_username(request):
    form = ChangeUsernameForm(user=request.user)
    if request.method == 'POST':
        form = ChangeUsernameForm(request.POST, user=request.user)
        if form.is_valid():
            request.user.username = form.cleaned_data['username']
            request.user.save()
            messages.success(request, 'You have successfully changed your username')
    return render(request, "account/change_user.html", {'form': form, 'notif_count': get_count(request)})


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
    return render(request, 'account/change_password.html', {'form': form, 'notif_count': get_count(request)})


@login_required
def change_email(request):
    form = ChangeEmailForm(user=request.user)
    if request.method == 'POST':
        form = ChangeEmailForm(request.POST, user=request.user)
        if form.is_valid():
            request.user.email = form.cleaned_data['email']
            request.user.save()
            messages.success(request, 'You have successfully changed your email')
    return render(request, 'account/change_email.html', {'form': form, 'notif_count': get_count(request)})


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
    return render(request, 'account/change_profile_pic.html', {'form': form, 'notif_count': get_count(request)})