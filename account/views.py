from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as user_login, logout as user_logout
from django.contrib.auth.forms import AuthenticationForm
from .models import CustomUser
from .forms import RegisterForm
from django.conf import settings
# Create your views here.


@login_required
def profile(request, username):
    user = get_object_or_404(CustomUser, username=username)
    print(settings.STATIC_URL)
    return render(request, 'account/profile.html', {"viewed_user": user})


def login(request):
    if request.user.is_authenticated:
        return redirect('/' + request.user.username)
    form = AuthenticationForm()
    if request.POST.get('submit') == 'log in':
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
    if request.POST.get('submit') == 'sign up':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    return render(request, "account/register.html", {'form': form})